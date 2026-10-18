#!/usr/bin/env python3
"""Hermes Agent 记忆备份脚本 — 备份到 bestwsl/openclaw-skills 仓库（GitHub API 方式，大陆网络可用）。

- 备份内容：memory store (MEMORY.md / USER.md)、SOUL.md、config.yaml(脱敏)、skills 清单、追踪脚本
- 推送方式：GitHub REST API PUT /contents/（git push 在大陆网络不稳定，见旧记忆）
- Token：读取环境变量 GITHUB_PAT 或文件 D:\\Hermes\\scripts\\github_token.txt
"""
import base64
import json
import os
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request

REPO = "bestwsl/openclaw-skills"
BRANCH = "main"
HERMES_HOME = os.environ.get("HERMES_HOME", r"D:\Hermes")
SCRIPTS_DIR = os.path.join(HERMES_HOME, "scripts")
TOKEN_FILE = os.path.join(SCRIPTS_DIR, "github_token.txt")
API = "https://api.github.com"

SOURCES = [
    (os.path.join(HERMES_HOME, "memories", "MEMORY.md"), "hermes-backup/MEMORY.md"),
    (os.path.join(HERMES_HOME, "memories", "USER.md"), "hermes-backup/USER.md"),
    (os.path.join(HERMES_HOME, "SOUL.md"), "hermes-backup/SOUL.md"),
    (os.path.join(HERMES_HOME, "config.yaml"), "hermes-backup/config.yaml"),
]


def get_token():
    token = os.environ.get("GITHUB_PAT", "").strip()
    if not token and os.path.exists(TOKEN_FILE):
        token = open(TOKEN_FILE, encoding="utf-8").read().strip()
    return token


def collect_files(tmp_dir):
    """构建待备份文件清单：复制到临时目录。返回所有待上传文件的 (full_path, repo_path) 列表。"""
    # 1) 核心记忆文件
    for src, rel in SOURCES:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(tmp_dir, os.path.basename(rel)))
    # 2) skills 清单
    skills_list = []
    skills_root = os.path.join(HERMES_HOME, "skills")
    if os.path.isdir(skills_root):
        for root, dirs, files in os.walk(skills_root):
            if "SKILL.md" in files:
                rel = os.path.relpath(root, skills_root)
                skills_list.append(rel.replace("\\", "/"))
    with open(os.path.join(tmp_dir, "skills-list.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(skills_list)))
    # 3) 追踪脚本（排除敏感文件：token/密钥，绝不能推送到公开仓库）
    if os.path.isdir(SCRIPTS_DIR):
        shutil.copytree(SCRIPTS_DIR, os.path.join(tmp_dir, "scripts"), dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('github_token.txt', '*.token', '*.key', '*.pem', '*.env', '.env'))
    # 4) 备份时间戳
    with open(os.path.join(tmp_dir, "last-backup.txt"), "w", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    # 返回所有待上传文件
    files = []
    for root, dirs, fnames in os.walk(tmp_dir):
        for fn in fnames:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, tmp_dir).replace("\\", "/")
            files.append((full, f"hermes-backup/{rel}"))
    return files


def api_request(method, url, token, body=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "hermes-backup")
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def push_file(token, local_path, repo_path):
    """通过 API 上传/更新单个文件。返回 (ok, detail)。"""
    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()
    # 获取远程现有 sha
    sha = None
    status, data = api_request("GET", f"{API}/repos/{REPO}/contents/{repo_path}?ref={BRANCH}", token)
    if status == 200:
        sha = data.get("sha")
    body = {
        "message": f"🔄 Hermes 记忆备份 {time.strftime('%Y-%m-%d %H:%M')}",
        "content": content_b64,
        "branch": BRANCH,
    }
    if sha:
        body["sha"] = sha
    status, data = api_request("PUT", f"{API}/repos/{REPO}/contents/{repo_path}", token, body)
    return status in (200, 201), f"{repo_path} -> {status}"


def main():
    token = get_token()
    if not token:
        print("❌ 未找到 GitHub PAT token：请设置环境变量 GITHUB_PAT 或写入 D:\\Hermes\\scripts\\github_token.txt")
        sys.exit(1)
    tmp_dir = tempfile.mkdtemp(prefix="hermes_backup_")
    try:
        files = collect_files(tmp_dir)
        if not files:
            print("⚠️ 没有找到可备份的文件")
            return
        results = [push_file(token, local, rel) for local, rel in files]
        ok = sum(1 for r in results if r[0])
        print(f"✅ 备份完成：{ok}/{len(files)} 个文件已推送到 {REPO}")
        for ok_flag, detail in results:
            if not ok_flag:
                print(f"   ⚠️ 失败: {detail}")
        if ok < len(files):
            sys.exit(1)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
