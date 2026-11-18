# ファイアレッド Gunk 移植版（日本版ファイアレッド用）のソース

Pokémon Gunk's FireRed（OnionGunk/pokemon-gunks-firered v1.4）の機能を、日本版ファイアレッドに移植した改造のソース一式です。FireRed & LeafGreen+（Deokishisu）の一部の機能も入っています。

日本版のデコンプは無いため、日本版後期版（Rev1）のROMに直接手を入れる方式です。

- 海外版用のソース（pret/pokefirered と Gunk のソース）を部分的にコンパイルします。
- できたプログラムを、日本版の空き領域や使われていない関数の場所に置きます。
- 日本版の関数から、置いたプログラムへ飛ぶようにつなぎます。

ROMのデータそのものは含んでいません。

## 中身

| フォルダ・ファイル | 内容 |
| --- | --- |
| `port-overlay/` | pret/pokefirered に上書き・追加するファイル。日本版用のフック（`src/hooks/`）、スクリプト（`data/hooks/`）、連れ歩き、使う Gunk の関数の一覧（`gx/features.cfg`）など |
| `gunk-jp.patch` | Gunk のソースへの変更。ボックスを69バイトで詰めて16箱を元の大きさに収める変更、自転車ギアのB切り替えなど |
| `tools/` | 対応表づくり（`match.py`・`propagate2.py`・`datawalk.py`・`syms.py`）、Gunk の関数の取り出し（`extract.py`・`gxbuild.py`）、リンク（`build_port.py`）、ROMへの書き込み（`patch_port.py`）、IPS作成（`mkips.py`）、一括ビルド（`mk.sh`）、比較テスト（`cmprun.py`・`boxtest.py`） |
| `symbols/` | 海外版と日本版の関数・データのアドレス対応表 |
| `emu/gbarun.c` | テスト用の mGBA ハーネス |
| `tests/` | 海外版 Gunk と見比べるテストの操作手順 |
| `bugnotes.txt` | 直したバグのメモ |

## 組み立て方

1. pret/pokefirered をコミット `ce6406d8c2eaf46d543c8a2606de0c3cb1951982` で `/home/claude/port` に置き、agbcc を入れます。
2. `port-overlay/` の中身を上書きします。
3. Gunk（OnionGunk/pokemon-gunks-firered、コミット `da541c9fa7d6bd2ce75c8b110db464e6aae5bc6d`）を `/home/claude/gunk` に置き、`gunk-jp.patch` を当てます。
4. 対応表を `/home/claude/work/amap.pkl` に置きます。
5. 次の2つを置きます。
   - 日本版後期版のROM：`/home/claude/roms/Pocket Monsters - FireRed (Japan) (Rev 1).gba`
   - pret でビルドした海外版のROM
6. `tools/mk.sh` を実行すると、`/home/claude/work/port.gba` ができます。

ツールのパスは上の置き場所を前提にしています。

## 151匹揃う版（別版）
- ビルド: `tools/mk151.sh`（通常版と同じ物＋`port-overlay/v151`。通常版の中身は変わらない）
- リーフグリーンの野生（草むら・なみのり・いわくだき・つり）が半分の確率で出る／ぶんぷにも出る
- 交換専用のカモネギ・ベロリンガ・ルージュラ・バリヤードを野生に追加
- フシギダネ・ヒトカゲ・ゼニガメ（Lv10）を3人のNPCがくれる、イーブイ3匹、サワムラー・エビワラー両方、カセキ両方
- ミュウ Lv50（ポケモンやしき B1F の日記、捕まえるまで何度でも）、ゲームコーナーにカイロス（2500枚）、タマムシ4Fでつきのいし（2100円）
- 151匹の入手方法: `docs/151_table.md`（`tools/check151.py` で作成、もれなし）
