import re
from pathlib import Path
import streamlit as st
import pandas as pd

# ページの基本設定
st.set_page_config(
    page_title="ドラゴンクエスト データベース",
    page_icon="⚔️",
    layout="wide"
)

# app.pyと同じ場所のdataフォルダ、または直下のどちらからでも読み込む設定
BASE_DIR = Path(__file__).resolve().parent

# データの読み込み
@st.cache_data
def load_data(filename):
    if (BASE_DIR / "data" / filename).exists():
        file_path = BASE_DIR / "data" / filename
    else:
        file_path = BASE_DIR / filename
    return pd.read_csv(file_path)

spells_df = load_data("spells.csv")
items_df = load_data("items.csv")
monsters_df = load_data("monsters.csv")
characters_df = load_data("characters.csv")

# ==========================================
# ドット絵イラスト（SVG）自動生成エンジン
# ==========================================
SPRITES = {
    "HERO": [
        "....YYYY....",
        "...YYYYYY...",
        "...YWWWWY...",
        "...WKWWKW...",
        "....WWWW....",
        "..RBBBBBBY..",
        ".RRBBBBBBYY.",
        "RR.BBBBBB.YY",
        "...BBBBBB...",
        "...BB..BB...",
        "..BB....BB..",
        "............"
    ],
    "WARRIOR": [
        "....RRRR....",
        "...RRRRRR...",
        "...WWWWWW...",
        "...WKWWKW...",
        "....WWWW....",
        ".BBBBBBBBBB.",
        "WW.BBBBBB.WW",
        "WW.BBBBBB.WW",
        "...BBBBBB...",
        "...BB..BB...",
        "..SS....SS..",
        "............"
    ],
    "MAGE": [
        ".....PP.....",
        "....PPPP....",
        "...PPPPPP...",
        "..PPPPPPPP..",
        "...WKWWKW...",
        "....WWWW....",
        "..YPPPPPP...",
        ".YYPPPPPPP..",
        ".Y.PPPPPP...",
        ".Y.PPPPPP...",
        "...PP..PP...",
        "............"
    ],
    "PRIEST": [
        "....WWWW....",
        "...WWWWWW...",
        "..WWYYYYWW..",
        "..WWKWWKWW..",
        "...WWWWWW...",
        "..GGGGGGGG..",
        ".GGGGGGGGGG.",
        "WW.GGGGGG.WW",
        "...GGGGGG...",
        "...GG..GG...",
        "..GG....GG..",
        "............"
    ],
    "SLIME": [
        ".....YY.....",
        "....YYYY....",
        ".....BB.....",
        "....BBBB....",
        "..BBBBBBBB..",
        ".BBBBBBBBBB.",
        "BBBWBBBBWBBB",
        "BBBKBWBBKBBB",
        "BBBBBBBBBBBB",
        "BBRBBBBBBBRB",
        ".BBRRRRRRBB.",
        "..BBBBBBBB.."
    ],
    "DRAGON": [
        "......GGG...",
        ".....GGWGG..",
        "....GGGGGGG.",
        "..GGGG..GGG.",
        ".GGGGGG.....",
        "GGGGGGGG....",
        "G.GGGGGG.GG.",
        "..GGGGGGGG..",
        ".GGGG..GGGG.",
        "GGG......GGG",
        "GG........GG",
        "............"
    ],
    "BEAST": [
        ".BB......BB.",
        "BBBB....BBBB",
        ".BBBBBBBBBB.",
        ".BBWBBBBWBB.",
        ".BBKBBBBKBB.",
        "..BBBBBBBB..",
        "..BBBRRBBB..",
        ".BBBBBBBBBB.",
        "BBB.BBBB.BBB",
        "BB..BBBB..BB",
        "....BB.BB...",
        "............"
    ],
    "DEMON": [
        ".YY......YY.",
        "..YY.RR.YY..",
        "...RRRRRR...",
        "..RRWWRRWWR.",
        "..RRRRRRRR..",
        ".RRRRRRRRRR.",
        "RR.RRRRRR.RR",
        "RR.RRRRRR.RR",
        "...RRRRRR...",
        "..RRR..RRR..",
        ".RRR....RRR.",
        "............"
    ],
    "UNDEAD": [
        "....WWWW....",
        "...WWWWWW...",
        "..WWKWWKWW..",
        "..WWWWWWWW..",
        "...WWKKWW...",
        "....WWWW....",
        "..WWWWWWWW..",
        ".WW.WWWW.WW.",
        "WW..WWWW..WW",
        "....WW.WW...",
        "...WW...WW..",
        "............"
    ],
    "CHEST": [
        "............",
        "..BBBBBBBB..",
        ".BYYYYYYYYB.",
        ".BYYYYYYYYB.",
        "BBBBYYYYBBBB",
        "BWWWWYYWWWWB",
        "BWWWWKKWWWWB",
        "BBBBBBBBBBBB",
        ".BBBBBBBBBB.",
        ".BBBBBBBBBB.",
        "............",
        "............"
    ],
    "MACHINE": [
        "....SSSS....",
        "...SRRRRS...",
        "..SSSSSSSS..",
        ".SS.SSSS.SS.",
        "WSS.SSSS.SSW",
        "WSS.SSSS.SSW",
        ".SS.SSSS.SS.",
        "....SSSS....",
        "...SS..SS...",
        "..SS....SS..",
        ".SS......SS.",
        "............"
    ],
    "BOSS": [
        "..YY.YY.YY..",
        "..YYYYYYYY..",
        "...PPPPPP...",
        "..PPYPPYPP..",
        ".PPPPPPPPPP.",
        "PPPPPPPPPPPP",
        "PP.PPPPPP.PP",
        "PP.PPPPPP.PP",
        "...PPPPPP...",
        "..PPP..PPP..",
        ".PPP....PPP.",
        "............"
    ],
    "SWORD": [
        ".........WW.",
        "........WWW.",
        ".......WWW..",
        "......WWW...",
        ".....WWW....",
        "....WWW.....",
        "..YYWWW.....",
        "...YYY......",
        "..BBYYY.....",
        ".BB..YY.....",
        "BB..........",
        "............"
    ],
    "STAFF": [
        "........RRR.",
        ".......RRRRR",
        ".......RRRRR",
        "........RRR.",
        ".......BB...",
        "......BB....",
        ".....BB.....",
        "....BB......",
        "...BB.......",
        "..BB........",
        ".BB.........",
        "............"
    ],
    "ARMOR": [
        "..BB....BB..",
        ".BBBB..BBBB.",
        "BBBBBBBBBBBB",
        "BBBBYYYYBBBB",
        ".BBBBBBBBBB.",
        ".BBBBYYYYBB.",
        ".BBBBBBBBBB.",
        ".BBBBBBBBBB.",
        "..BBBBBBBB..",
        "..BBBBBBBB..",
        "............",
        "............"
    ],
    "SHIELD": [
        "............",
        "..YYYYYYYY..",
        ".YBBBBBBBBY.",
        ".YBBYYYYBBY.",
        ".YBBYBBYBBY.",
        ".YBBYYYYBBY.",
        ".YBBBBBBBBY.",
        "..YBBBBBBY..",
        "...YBBBBY...",
        "....YBBY....",
        ".....YY.....",
        "............"
    ],
    "HELM": [
        "....YYYY....",
        "...BBBBBB...",
        "..BBBBBBBB..",
        ".BBBBBBBBBB.",
        ".BBYYYYYYBB.",
        ".BBKBBBBKBB.",
        ".BBKBBBBKBB.",
        "..BB....BB..",
        "............",
        "............",
        "............",
        "............"
    ],
    "RING": [
        "............",
        ".....RR.....",
        "....RRRR....",
        ".....RR.....",
        "...YYYYYY...",
        "..YY....YY..",
        "..YY....YY..",
        "..YY....YY..",
        "...YYYYYY...",
        "............",
        "............",
        "............"
    ],
    "FIRE": [
        ".....RR.....",
        "....RRRR....",
        "...RRRRRR...",
        "..RRYYYYRR..",
        ".RRRYYYYRRR.",
        ".RRYYYYYYRR.",
        "RRRYYWWYYRRR",
        "RRRYYWWYYRRR",
        ".RRRYYYYRRR.",
        "..RRRRRRRR..",
        "...RRRRRR...",
        "............"
    ],
    "ICE": [
        ".....WW.....",
        "..W..CC..W..",
        "...WCCCCW...",
        ".W..CCCC..W.",
        "..CCCCCCCC..",
        "WWCCCCCCCCWW",
        "..CCCCCCCC..",
        ".W..CCCC..W.",
        "...WCCCCW...",
        "..W..CC..W..",
        ".....WW.....",
        "............"
    ],
    "THUNDER": [
        "......YYYY..",
        ".....YYYY...",
        "....YYYY....",
        "...YYYY.....",
        "..YYYYYYYY..",
        ".....YYYY...",
        "....YYYY....",
        "...YYYY.....",
        "..YYYY......",
        ".YYYY.......",
        "............",
        "............"
    ],
    "WIND": [
        "..GGGGGGGG..",
        ".GGGGGGGGGG.",
        "GG........GG",
        "..GGGGGGGG..",
        "...GGGGGG...",
        "....GGGG....",
        ".....GG.....",
        "....GGGG....",
        ".....GG.....",
        "............",
        "............",
        "............"
    ],
    "EXPLOSION": [
        "..Y..RR..Y..",
        "...RRRRRR...",
        ".YRRYYYYRRY.",
        "..RRYYYYRR..",
        "RRRYYWWYYRRR",
        "RRRYYWWYYRRR",
        "..RRYYYYRR..",
        ".YRRYYYYRRY.",
        "...RRRRRR...",
        "..Y..RR..Y..",
        "............",
        "............"
    ],
    "HEAL": [
        "............",
        "..RR....RR..",
        ".RRRR..RRRR.",
        "RRRRRRRRRRRR",
        "RRRRRRRRRRRR",
        ".RRRRRRRRRR.",
        "..RRRRRRRR..",
        "...RRRRRR...",
        "....RRRR....",
        ".....RR.....",
        "............",
        "............"
    ],
    "MAGIC": [
        ".....YY.....",
        "....YYYY....",
        "..CC.YY.CC..",
        ".CCCC..CCCC.",
        "YY..CCCC..YY",
        "YY..CCCC..YY",
        ".CCCC..CCCC.",
        "..CC.YY.CC..",
        "....YYYY....",
        ".....YY.....",
        "............",
        "............"
    ],
    "SLASH": [
        ".........WW.",
        "........WWW.",
        ".......WWW..",
        "......WWW...",
        ".....WWW....",
        "....CCC.....",
        "...CCC......",
        "..CCC.......",
        ".CC.........",
        "CC..........",
        "............",
        "............"
    ]
}

def render_pixel_art(sprite_key, overrides=None, size=68):
    base_palette = {
        "B": "#2979ff",  # 青
        "R": "#ff3d00",  # 赤
        "Y": "#ffd600",  # 黄・金
        "G": "#00c853",  # 緑
        "C": "#00e5ff",  # 水色
        "P": "#aa00ff",  # 紫
        "S": "#b0bec5",  # 銀
        "W": "#ffffff",  # 白
        "K": "#111111",  # 黒
    }
    if overrides:
        base_palette.update(overrides)

    grid = SPRITES.get(sprite_key, SPRITES["MAGIC"])
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch != "." and ch in base_palette:
                color = base_palette[ch]
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{color}"/>')

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" '
        f'width="{size}" height="{size}" shape-rendering="crispEdges" '
        f'style="background:#1c2233; border:2px solid #4a5568; border-radius:6px; padding:4px;">'
        f'{"".join(rects)}</svg>'
    )
    return svg

def get_role_group(role):
    r = str(role)
    if "将軍" in r:
        return "戦士・武闘家・盗賊"
    elif "勇者" in r or "英雄" in r:
        return "勇者・英雄"
    elif any(w in r for w in ["魔法", "魔導", "占い", "賢者"]):
        return "魔法使い・賢者"
    elif any(w in r for w in ["僧侶", "神官", "聖女", "旅芸人", "商人", "妖精"]):
        return "僧侶・サポート"
    else:
        return "戦士・武闘家・盗賊"

def get_character_svg(row, size=68):
    name = str(row["名前"])
    group = get_role_group(row["職業・役割"])
    if group == "勇者・英雄":
        override = {"W": "#ffccbc", "Y": "#ffd600", "B": "#2979ff", "R": "#ff3d00"}
        if "ソロ" in name or "レック" in name or "エイト" in name:
            override["Y"] = "#5d4037"  # 茶髪・黒髪系
        return render_pixel_art("HERO", override, size=size)
    elif group == "魔法使い・賢者":
        override = {"W": "#ffccbc", "P": "#aa00ff", "Y": "#ffd600"}
        if "ゼシカ" in name or "マーニャ" in name or "ベロニカ" in name:
            override["P"] = "#ff1744"
        elif "ブライ" in name or "ロウ" in name:
            override["P"] = "#00b0ff"
        return render_pixel_art("MAGE", override, size=size)
    elif group == "僧侶・サポート":
        override = {"W": "#ffccbc", "G": "#00c853", "Y": "#ffd600"}
        if "シルビア" in name or "トルネコ" in name:
            override["G"] = "#ff9100"
        return render_pixel_art("PRIEST", override, size=size)
    else:
        override = {"W": "#ffccbc", "B": "#d84315", "R": "#ffd600", "S": "#90a4ae"}
        if "カミュ" in name or "テリー" in name:
            override["R"] = "#00e5ff"
            override["B"] = "#1e88e5"
        elif "ピサロ" in name:
            override["R"] = "#eceff1"
            override["B"] = "#6a1b9a"
        return render_pixel_art("WARRIOR", override, size=size)

def get_spell_svg(row, size=68):
    attr = str(row["属性"])
    cat = str(row["分類"])
    if attr == "メラ" or attr == "ギラ":
        return render_pixel_art("FIRE", size=size)
    elif attr == "ヒャド":
        return render_pixel_art("ICE", size=size)
    elif attr == "デイン":
        return render_pixel_art("THUNDER", size=size)
    elif attr == "バギ":
        return render_pixel_art("WIND", size=size)
    elif attr == "イオ" or "マダンテ" in str(row["名前"]):
        return render_pixel_art("EXPLOSION", size=size)
    elif attr == "ドルマ":
        return render_pixel_art("MAGIC", {"C": "#aa00ff", "Y": "#ff4081"}, size=size)
    elif attr in ["回復", "蘇生"]:
        color = "#ff4081" if attr == "回復" else "#00e676"
        return render_pixel_art("HEAL", {"R": color}, size=size)
    elif cat == "特技":
        return render_pixel_art("SLASH", size=size)
    else:
        return render_pixel_art("MAGIC", size=size)

def get_item_svg(row, size=68):
    name = str(row["名前"])
    kind = str(row["種類"])
    if kind == "武器":
        if any(w in name for w in ["つえ", "杖", "ムチ", "かなづち", "ハンマー", "ブーメラン", "ウィング"]):
            color = "#00e5ff" if "メタル" in name else "#ff5252"
            return render_pixel_art("STAFF", {"R": color, "B": "#8d6e63"}, size=size)
        override = {"W": "#e0f7fa", "Y": "#ffd600", "B": "#2979ff"}
        if "ほのお" in name or "いなずま" in name:
            override["W"] = "#ff7043"
        elif "ふぶき" in name:
            override["W"] = "#4fc3f7"
        elif "メタル" in name or "ぎんが" in name:
            override["W"] = "#eceff1"
            override["Y"] = "#90a4ae"
        return render_pixel_art("SWORD", override, size=size)
    elif kind == "防具":
        if "たて" in name or "シールド" in name:
            color = "#cfd8dc" if "メタル" in name else "#2979ff"
            return render_pixel_art("SHIELD", {"B": color}, size=size)
        elif any(w in name for w in ["ぼうし", "ヘルム", "かぶと", "ティアラ", "マスク"]):
            color = "#cfd8dc" if "メタル" in name else "#ff9100"
            return render_pixel_art("HELM", {"B": color}, size=size)
        override = {"B": "#2979ff", "Y": "#ffd600"}
        if "メタル" in name:
            override["B"] = "#cfd8dc"
        elif "みずの" in name:
            override["B"] = "#00e5ff"
        elif "ひかり" in name or "プリンセス" in name or "シルク" in name:
            override["B"] = "#f48fb1"
        return render_pixel_art("ARMOR", override, size=size)
    else:
        color = "#00e676" if "めがみ" in name or "ソーサリー" in name else "#ff1744"
        return render_pixel_art("RING", {"R": color}, size=size)

def get_monster_svg(row, size=68):
    name = str(row["名前"])
    family = str(row["系統"])
    if family == "スライム系":
        override = {"B": "#2979ff", "Y": "#1c2233"}
        if "ベス" in name:
            override["B"] = "#ff6d00"
        elif "バブル" in name:
            override["B"] = "#00c853"
        elif "ホイミ" in name or "ベホマ" in name:
            override["B"] = "#40c4ff"
        elif "メタル" in name or "プラチナ" in name:
            override["B"] = "#cfd8dc"
        elif "ゴールデン" in name:
            override["B"] = "#ffd600"
        if any(w in name for w in ["キング", "クイーン", "エンペラー"]):
            override["Y"] = "#ffd600"
        return render_pixel_art("SLIME", override, size=size)
    elif family == "ドラゴン系":
        color = "#ff5252" if "ダース" in name else ("#546e7a" if "ブラック" in name else "#00c853")
        return render_pixel_art("DRAGON", {"G": color}, size=size)
    elif family == "魔獣系":
        return render_pixel_art("BEAST", {"B": "#d84315"}, size=size)
    elif family == "悪魔系":
        return render_pixel_art("DEMON", size=size)
    elif family == "ゾンビ系":
        return render_pixel_art("UNDEAD", size=size)
    elif family == "物質系":
        color = "#ffd600" if "ゴールド" in name or "ほうせき" in name else "#8d6e63"
        return render_pixel_art("CHEST", {"B": color}, size=size)
    elif family == "マシン系":
        color = "#ff5252" if "スーパー" in name or "2" in name else "#b0bec5"
        return render_pixel_art("MACHINE", {"S": color}, size=size)
    else:
        return render_pixel_art("BOSS", size=size)

# 作品名の精密マッチング関数
def match_series(text, series_name):
    if pd.isna(text):
        return False
    pattern = rf"(?<![0-9]){re.escape(series_name)}(?![0-9])"
    return bool(re.search(pattern, str(text)))

# --- ヘッダー＆ダッシュボード ---
st.title("⚔️ ドラゴンクエスト シリーズまとめ図鑑")
st.caption("ドット絵イラスト＆ステータス検索対応のオリジナルデータベースです。")

total_count = len(spells_df) + len(items_df) + len(monsters_df) + len(characters_df)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🔥 呪文・特技", f"{len(spells_df)} 件")
col2.metric("🛡️ 装備品", f"{len(items_df)} 件")
col3.metric("👾 魔物図鑑", f"{len(monsters_df)} 件")
col4.metric("🧑 キャラクター", f"{len(characters_df)} 名")
col5.metric("📚 総データ数", f"{total_count} 件")

st.divider()

# --- サイドバー：検索・絞り込み・表示設定 ---
st.sidebar.header("🔍 検索・絞り込み")
keyword = st.sidebar.text_input("キーワード検索", placeholder="例：メラ、ロト、アリーナ、スライム")

series_list = ["すべて", "DQ1", "DQ2", "DQ3", "DQ4", "DQ5", "DQ6", "DQ7", "DQ8", "DQ9", "DQ10", "DQ11"]
selected_series = st.sidebar.selectbox("🎮 登場作品で絞り込み", series_list)

include_unlisted_items = st.sidebar.checkbox(
    "作品記載のない汎用装備も表示する",
    value=True
)

st.sidebar.divider()
st.sidebar.header("⚙️ 表示設定")
view_mode = st.sidebar.radio(
    "表示スタイル",
    ["カード表示（ドット絵イラスト付き）", "一覧表（コンパクト＋図鑑ビューア）"]
)

def filter_by_keyword(df, kw):
    if not kw:
        return df
    return df[
        df.apply(
            lambda row: kw.lower() in row.astype(str).str.lower().str.cat(sep=" "),
            axis=1
        )
    ]

# --- メインコンテンツ ---
tab1, tab2, tab3, tab4 = st.tabs(["🔥 呪文・特技", "🛡️ 装備品", "👾 魔物図鑑", "🧑 キャラクター"])

# ==========================================
# タブ1：呪文・特技
# ==========================================
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        categories = spells_df["分類"].unique().tolist()
        selected_cat = st.multiselect("分類で絞り込み", categories, default=categories)
    with c2:
        elements = spells_df["属性"].unique().tolist()
        selected_elem = st.multiselect("属性で絞り込み", elements, default=elements)

    filtered_spells = spells_df[
        (spells_df["分類"].isin(selected_cat)) &
        (spells_df["属性"].isin(selected_elem))
    ]
    if selected_series != "すべて":
        filtered_spells = filtered_spells[
            filtered_spells["登場作品"].apply(lambda x: match_series(x, selected_series))
        ]
    filtered_spells = filter_by_keyword(filtered_spells, keyword)

    st.write(f"該当件数: **{len(filtered_spells)}** 件")

    if len(filtered_spells) == 0:
        st.info("条件に一致する呪文・特技が見つかりませんでした。")
    elif view_mode == "カード表示（ドット絵イラスト付き）":
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_spells.iterrows()):
            with cols[idx % 2]:
                svg = get_spell_svg(row, size=68)
                st.markdown(f"""
                <div class="dq-window">
                    <div style="display:flex; gap:14px; align-items:center;">
                        <div>{svg}</div>
                        <div style="flex:1;">
                            <div class="dq-title">{row['名前']}</div>
                            <div>
                                <span class="dq-badge">{row['分類']}</span>
                                <span class="dq-badge">{row['属性']}</span>
                            </div>
                            <div class="dq-stat">消費MP: <b>{row['消費MP']}</b> ／ 登場: {row['登場作品']}</div>
                        </div>
                    </div>
                    <div class="dq-desc" style="margin-top:8px;">{row['効果']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        pick_spell = st.selectbox("🖼️ イラスト図鑑ビューア（選択してイラスト表示）", filtered_spells["名前"].tolist())
        row = filtered_spells[filtered_spells["名前"] == pick_spell].iloc[0]
        svg = get_spell_svg(row, size=84)
        st.markdown(f"""
        <div class="dq-window">
            <div style="display:flex; gap:16px; align-items:center;">
                <div>{svg}</div>
                <div style="flex:1;">
                    <div class="dq-title">{row['名前']} <span class="dq-badge">{row['分類']}</span> <span class="dq-badge">{row['属性']}</span></div>
                    <div class="dq-stat">消費MP: <b>{row['消費MP']}</b> ／ 登場作品: {row['登場作品']}</div>
                    <div class="dq-desc">{row['効果']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered_spells, use_container_width=True, hide_index=True)

# ==========================================
# タブ2：装備品
# ==========================================
with tab2:
    c1, c2 = st.columns([2, 1])
    with c1:
        item_types = items_df["種類"].unique().tolist()
        selected_types = st.multiselect("種類で絞り込み", item_types, default=item_types)
    with c2:
        item_sort = st.selectbox("並び替え", ["登録順", "攻撃力・守備力が高い順", "攻撃力・守備力が低い順"])

    filtered_items = items_df[items_df["種類"].isin(selected_types)]
    if selected_series != "すべて":
        has_dq_tag = filtered_items["主な入手方法"].str.contains("DQ", na=False)
        matched_series = filtered_items["主な入手方法"].apply(lambda x: match_series(x, selected_series))
        if include_unlisted_items:
            filtered_items = filtered_items[matched_series | (~has_dq_tag)]
        else:
            filtered_items = filtered_items[matched_series]
    filtered_items = filter_by_keyword(filtered_items, keyword)

    if item_sort == "攻撃力・守備力が高い順":
        filtered_items = filtered_items.sort_values(by="攻撃力_守備力", ascending=False)
    elif item_sort == "攻撃力・守備力が低い順":
        filtered_items = filtered_items.sort_values(by="攻撃力_守備力", ascending=True)

    st.write(f"該当件数: **{len(filtered_items)}** 件")

    if len(filtered_items) == 0:
        st.info("条件に一致する装備品が見つかりませんでした。")
    elif view_mode == "カード表示（ドット絵イラスト付き）":
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_items.iterrows()):
            with cols[idx % 2]:
                svg = get_item_svg(row, size=68)
                stat_label = "攻撃力" if row["種類"] == "武器" else "守備力"
                st.markdown(f"""
                <div class="dq-window">
                    <div style="display:flex; gap:14px; align-items:center;">
                        <div>{svg}</div>
                        <div style="flex:1;">
                            <div class="dq-title">{row['名前']} <span class="dq-badge">{row['種類']}</span></div>
                            <div class="dq-stat">{stat_label}: <b>{row['攻撃力_守備力']}</b> ／ 入手: {row['主な入手方法']}</div>
                        </div>
                    </div>
                    <div class="dq-desc" style="margin-top:8px;">{row['特殊効果']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        pick_item = st.selectbox("🖼️ イラスト図鑑ビューア（選択してイラスト表示）", filtered_items["名前"].tolist())
        row = filtered_items[filtered_items["名前"] == pick_item].iloc[0]
        svg = get_item_svg(row, size=84)
        stat_label = "攻撃力" if row["種類"] == "武器" else "守備力"
        st.markdown(f"""
        <div class="dq-window">
            <div style="display:flex; gap:16px; align-items:center;">
                <div>{svg}</div>
                <div style="flex:1;">
                    <div class="dq-title">{row['名前']} <span class="dq-badge">{row['種類']}</span></div>
                    <div class="dq-stat">{stat_label}: <b>{row['攻撃力_守備力']}</b> ／ 主な入手方法: {row['主な入手方法']}</div>
                    <div class="dq-desc">{row['特殊効果']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered_items, use_container_width=True, hide_index=True)

# ==========================================
# タブ3：魔物図鑑
# ==========================================
with tab3:
    c1, c2 = st.columns([2, 1])
    with c1:
        families = monsters_df["系統"].unique().tolist()
        selected_families = st.multiselect("系統で絞り込み", families, default=families)
    with c2:
        monster_sort = st.selectbox(
            "並び替え",
            ["登録順", "経験値が高い順", "ゴールドが多い順", "HPが高い順", "HPが低い順"]
        )

    filtered_monsters = monsters_df[monsters_df["系統"].isin(selected_families)]
    filtered_monsters = filter_by_keyword(filtered_monsters, keyword)

    if monster_sort == "経験値が高い順":
        filtered_monsters = filtered_monsters.sort_values(by="経験値", ascending=False)
    elif monster_sort == "ゴールドが多い順":
        filtered_monsters = filtered_monsters.sort_values(by="ゴールド", ascending=False)
    elif monster_sort == "HPが高い順":
        filtered_monsters = filtered_monsters.sort_values(by="HP", ascending=False)
    elif monster_sort == "HPが低い順":
        filtered_monsters = filtered_monsters.sort_values(by="HP", ascending=True)

    st.write(f"該当件数: **{len(filtered_monsters)}** 件")

    if len(filtered_monsters) == 0:
        st.info("条件に一致する魔物が見つかりませんでした。")
    elif view_mode == "カード表示（ドット絵イラスト付き）":
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_monsters.iterrows()):
            with cols[idx % 2]:
                svg = get_monster_svg(row, size=68)
                st.markdown(f"""
                <div class="dq-window">
                    <div style="display:flex; gap:14px; align-items:center;">
                        <div>{svg}</div>
                        <div style="flex:1;">
                            <div class="dq-title">{row['名前']} <span class="dq-badge">{row['系統']}</span></div>
                            <div class="dq-stat">HP: <b>{row['HP']}</b> ／ 経験値: <b>{row['経験値']}</b> ／ G: <b>{row['ゴールド']}</b></div>
                        </div>
                    </div>
                    <div class="dq-desc" style="margin-top:8px;">{row['特徴・ドロップ']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        pick_monster = st.selectbox("🖼️ イラスト図鑑ビューア（選択してイラスト表示）", filtered_monsters["名前"].tolist())
        row = filtered_monsters[filtered_monsters["名前"] == pick_monster].iloc[0]
        svg = get_monster_svg(row, size=84)
        st.markdown(f"""
        <div class="dq-window">
            <div style="display:flex; gap:16px; align-items:center;">
                <div>{svg}</div>
                <div style="flex:1;">
                    <div class="dq-title">{row['名前']} <span class="dq-badge">{row['系統']}</span></div>
                    <div class="dq-stat">HP: <b>{row['HP']}</b> ／ 経験値: <b>{row['経験値']}</b> ／ ゴールド: <b>{row['ゴールド']}</b></div>
                    <div class="dq-desc">{row['特徴・ドロップ']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered_monsters, use_container_width=True, hide_index=True)

# ==========================================
# タブ4：キャラクター
# ==========================================
with tab4:
    role_groups = ["勇者・英雄", "戦士・武闘家・盗賊", "魔法使い・賢者", "僧侶・サポート"]
    selected_role_groups = st.multiselect("役割タイプで絞り込み", role_groups, default=role_groups)

    filtered_chars = characters_df[
        characters_df["職業・役割"].apply(get_role_group).isin(selected_role_groups)
    ]
    if selected_series != "すべて":
        filtered_chars = filtered_chars[
            filtered_chars["登場作品"].apply(lambda x: match_series(x, selected_series))
        ]
    filtered_chars = filter_by_keyword(filtered_chars, keyword)

    st.write(f"該当人数: **{len(filtered_chars)}** 名")

    if len(filtered_chars) == 0:
        st.info("条件に一致するキャラクターが見つかりませんでした。")
    elif view_mode == "カード表示（ドット絵イラスト付き）":
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_chars.iterrows()):
            with cols[idx % 2]:
                svg = get_character_svg(row, size=68)
                st.markdown(f"""
                <div class="dq-window">
                    <div style="display:flex; gap:14px; align-items:center;">
                        <div>{svg}</div>
                        <div style="flex:1;">
                            <div class="dq-title">{row['名前']}</div>
                            <div>
                                <span class="dq-badge">{row['登場作品']}</span>
                                <span class="dq-badge">{row['職業・役割']}</span>
                            </div>
                            <div class="dq-stat">得意武器・呪文: <b>{row['得意武器・呪文']}</b></div>
                        </div>
                    </div>
                    <div class="dq-desc" style="margin-top:8px;">{row['特徴・プロフィール']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        pick_char = st.selectbox("🖼️ イラスト図鑑ビューア（選択してイラスト表示）", filtered_chars["名前"].tolist())
        row = filtered_chars[filtered_chars["名前"] == pick_char].iloc[0]
        svg = get_character_svg(row, size=84)
        st.markdown(f"""
        <div class="dq-window">
            <div style="display:flex; gap:16px; align-items:center;">
                <div>{svg}</div>
                <div style="flex:1;">
                    <div class="dq-title">{row['名前']} <span class="dq-badge">{row['登場作品']}</span> <span class="dq-badge">{row['職業・役割']}</span></div>
                    <div class="dq-stat">得意武器・呪文: <b>{row['得意武器・呪文']}</b></div>
                    <div class="dq-desc">{row['特徴・プロフィール']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered_chars, use_container_width=True, hide_index=True)