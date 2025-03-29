from django.core.management.base import BaseCommand
from django.core.management import call_command, get_commands

class Command(BaseCommand):
    help = "プロジェクト内の全ての管理コマンド（自身を除く）を実行するコマンド"

    def handle(self, *_args, **_options):
        commands = get_commands()
        for name in sorted(commands.keys()):
            if name == "all":  # 本コマンド自体は除外
                continue
            self.stdout.write(f"コマンド '{name}' を実行中...")
            try:
                call_command(name)
            except Exception as e:
                self.stderr.write(f"コマンド '{name}' の実行に失敗しました: {e}")
        self.stdout.write("全てのコマンドの実行が完了しました。")