#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from datetime import datetime


def run_command(cmd, cwd=None, capture_output=False):
    """执行命令"""
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=capture_output,
                       text=True, check=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {cmd}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        sys.exit(1)


def get_current_branch():
    """获取当前分支"""
    result = run_command("git branch --show-current", capture_output=True)
    return result.stdout.strip()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__)) or '.'

    os.chdir(script_dir)

    print("🚀 自动部署脚本")
    print("=" * 40)

    # 检查是否在 git 仓库中
    if not os.path.exists(".git"):
        print("❌ 错误: 当前目录不是 git 仓库")
        sys.exit(1)

    # 获取当前分支
    branch = get_current_branch()
    print(f"📍 当前分支: {branch}")

    # 获取提交信息
    if len(sys.argv) > 1:
        commit_msg = " ".join(sys.argv[1:])
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"更新内容 - {now}"

    print(f"📝 提交信息: {commit_msg}")

    print("\n📋 检查 Git 状态...")
    run_command("git status")

    print("\n📦 添加更改...")
    run_command("git add .")

    # 检查是否有更改需要提交
    try:
        result = run_command("git diff --cached --quiet", capture_output=True)
        print("ℹ️ 没有需要提交的更改")
        return
    except subprocess.CalledProcessError:
        pass

    print("\n✅ 提交更改...")
    run_command(f'git commit -m "{commit_msg}"')

    print("\n🚀 推送到 GitHub...")
    run_command("git push origin new-personal-homepage")

    print("\n" + "=" * 40)
    print("✨ 部署完成！")


if __name__ == "__main__":
    main()
