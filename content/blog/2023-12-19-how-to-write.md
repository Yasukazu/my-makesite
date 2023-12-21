---
title: Front matter as markdown header i.e. YAML format part separated with 3 hyphens('---') before and after the header part
---
<!-- title: Front matter in HTML comment -->
## Difference from original *makesite*
- Originally, meta data (aka front matters) are set as comments of HTML.
- In this fork, meta data are written in leading 3-hyphen separated part as YAML format(YAML format is like a simplified JSON format).

## Notice:
- Headings start from H2 aka double crosshatches

## About settings
 Since H1 is set with `title` in the front matter.
作者が言うには，サイトが生成される過程を分かりやすくするために一個のPythonスクリプトで作ったとのこと。
Author explains that `makesite.py` is made simple to clarify building site.

## ２種類の設定値埋め込み:設定と読み出し
 - `content` フォルダ内の HTML ファイルには HTML には記述されない設定名と値の対(別名メタデータ)を設定する方法として「HTMLのコメント用タグ」に設定名と値をコロン記号で区切って記入する: ```<!-- 設定名:値 -->```
 - `layout` フォルダ内の HTML ファイルでは値を読み出して埋め込む場所に設定名を二重波カッコで囲んで記入する: ```{{設定名}}```
