import streamlit as st
import json
import os
import csv
import base64
import requests
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Soccer Stats Tracker",
    page_icon="⚽",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main { background: #0b1a0e; }
.block-container { padding: 4rem 6rem 4rem; max-width: 1200px; }

/* ── Title ── */
.app-title {
    font-family: 'Oswald', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #e8f5e9;
    letter-spacing: 2px;
    line-height: 1;
}
.app-sub {
    color: #4caf50;
    font-size: 0.8rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 5px;
}

/* ── Stat cards ── */
.stat-card {
    background: #132218;
    border: 1px solid #1e3a23;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.stat-number {
    font-family: 'Oswald', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #4caf50;
    line-height: 1;
}
.stat-label {
    font-size: 0.68rem;
    color: #6a9e6e;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
}
.stat-sub {
    font-size: 0.72rem;
    color: #3a6b3e;
    margin-top: 2px;
}

/* ── Goalie stat card (accent in gold/amber) ── */
.stat-card-goalie {
    background: #1a1a0e;
    border: 1px solid #3a3a1e;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
}
.stat-number-goalie {
    font-family: 'Oswald', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffc107;
    line-height: 1;
}
.stat-label-goalie {
    font-size: 0.68rem;
    color: #a08030;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* ── Event buttons ── */
.event-section {
    background: #0f2214;
    border: 1px solid #1e3a23;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.event-section-goalie {
    background: #14140a;
    border: 1px solid #3a3a1e;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.event-section-title {
    font-family: 'Oswald', sans-serif;
    font-size: 0.85rem;
    color: #4caf50;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.event-section-title-goalie {
    font-family: 'Oswald', sans-serif;
    font-size: 0.85rem;
    color: #ffc107;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Activity log ── */
.log-entry {
    background: #0f2214;
    border-left: 3px solid #2e7d32;
    border-radius: 0 6px 6px 0;
    padding: 0.4rem 0.8rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    color: #a5d6a7;
    display: flex;
    justify-content: space-between;
}
.log-time { color: #3a6b3e; font-size: 0.75rem; }

/* ── Game header card ── */
.game-card {
    background: #132218;
    border: 1px solid #2e7d32;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1rem;
}
.game-title-text {
    font-family: 'Oswald', sans-serif;
    font-size: 1.4rem;
    color: #e8f5e9;
    letter-spacing: 1px;
}
.game-meta { font-size: 0.8rem; color: #4caf50; margin-top: 2px; }

/* ── Section divider ── */
.section-label {
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2e7d32;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}

/* ── Pass accuracy bar ── */
.accuracy-bar-bg {
    background: #1e3a23;
    border-radius: 4px;
    height: 8px;
    margin-top: 6px;
    overflow: hidden;
}
.accuracy-bar-fill {
    background: #4caf50;
    height: 8px;
    border-radius: 4px;
    transition: width 0.3s;
}

/* ── Save percentage bar (goalie) ── */
.save-bar-bg {
    background: #2a2a10;
    border-radius: 4px;
    height: 8px;
    margin-top: 6px;
    overflow: hidden;
}
.save-bar-fill {
    background: #ffc107;
    height: 8px;
    border-radius: 4px;
    transition: width 0.3s;
}

/* ── Saved games list ── */
.saved-game-row {
    background: #0f2214;
    border: 1px solid #1e3a23;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #a5d6a7;
}
.saved-game-date { color: #3a6b3e; font-size: 0.75rem; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: #132218 !important;
    color: #a5d6a7 !important;
    border: 1px solid #2e7d32 !important;
    border-radius: 8px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 0.8rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #1e3a23 !important;
    border-color: #4caf50 !important;
    color: #e8f5e9 !important;
}
div[data-testid="column"] .stButton > button {
    font-size: 0.85rem !important;
    padding: 0.6rem 0.4rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA STORAGE
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = "soccer_stats.json"
CSV_FILE  = "soccer_stats.csv"

# ─────────────────────────────────────────────────────────────────────────────
# GITHUB CSV SYNC
# ─────────────────────────────────────────────────────────────────────────────
CSV_COLUMNS = [
    "id", "saved_at", "date", "player", "opponent", "is_goalie",
    "goals", "assists", "passes_successful", "passes_unsuccessful",
    "pass_accuracy_pct", "shots_on_target", "shots_off_target",
    "shot_accuracy_pct", "steals", "interceptions", "clearances",
    "turnovers", "fouls_won", "fouls_committed",
    "saves", "goals_allowed", "goalie_clearances", "save_pct",
]

def _game_to_csv_row(game: dict) -> dict:
    s = game["stats"]
    total_passes = s["passes_successful"] + s["passes_unsuccessful"]
    pass_acc = round(s["passes_successful"] / total_passes * 100, 1) if total_passes else 0
    total_shots = s["shots_on_target"] + s["shots_off_target"]
    shot_acc = round(s["shots_on_target"] / total_shots * 100, 1) if total_shots else 0
    saves = s.get("saves", 0)
    goals_allowed = s.get("goals_allowed", 0)
    total_faced = saves + goals_allowed
    sv_pct = round(saves / total_faced * 100, 1) if total_faced else 0
    return {
        "id":                    game["id"],
        "saved_at":              game["saved_at"],
        "date":                  game["date"],
        "player":                game["player"],
        "opponent":              game["opponent"],
        "is_goalie":             game.get("is_goalie", False),
        "goals":                 s["goals"],
        "assists":               s["assists"],
        "passes_successful":     s["passes_successful"],
        "passes_unsuccessful":   s["passes_unsuccessful"],
        "pass_accuracy_pct":     pass_acc,
        "shots_on_target":       s["shots_on_target"],
        "shots_off_target":      s["shots_off_target"],
        "shot_accuracy_pct":     shot_acc,
        "steals":                s["steals"],
        "interceptions":         s["interceptions"],
        "clearances":            s["clearances"],
        "turnovers":             s["turnovers"],
        "fouls_won":             s["fouls_won"],
        "fouls_committed":       s["fouls_committed"],
        "saves":                 saves,
        "goals_allowed":         goals_allowed,
        "goalie_clearances":     s.get("goalie_clearances", 0),
        "save_pct":              sv_pct,
    }

def _build_csv_content(games: list) -> str:
    """Rebuild full CSV string from all games."""
    import io
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for g in games:
        writer.writerow(_game_to_csv_row(g))
    return buf.getvalue()

def push_csv_to_github(games: list) -> tuple[bool, str]:
    """
    Push the full CSV to GitHub (create or update soccer_stats.csv in repo root).
    Reads token + repo from st.secrets[github].
    Returns (success: bool, message: str).
    """
    try:
        token = st.secrets["github"]["token"]
        repo  = st.secrets["github"]["repo"]
    except Exception:
        return False, "GitHub secrets not configured. Add [github] token and repo to Streamlit secrets."

    csv_content = _build_csv_content(games)
    encoded = base64.b64encode(csv_content.encode()).decode()

    api_url = f"https://api.github.com/repos/{repo}/contents/{CSV_FILE}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # Check if file already exists to get its SHA (required for updates)
    sha = None
    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        if r.status_code == 200:
            sha = r.json().get("sha")
    except requests.RequestException:
        pass

    payload = {
        "message": f"stats: update soccer_stats.csv — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": encoded,
    }
    if sha:
        payload["sha"] = sha

    try:
        r = requests.put(api_url, headers=headers, json=payload, timeout=15)
        if r.status_code in (200, 201):
            return True, "✅ Stats pushed to GitHub"
        else:
            return False, f"GitHub API error {r.status_code}: {r.json().get('message', 'unknown error')}"
    except requests.RequestException as e:
        return False, f"Network error: {e}"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {"games": []}
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return {"games": []}
    return {"games": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "screen": "home",
        "player_name": "",
        "opponent": "",
        "game_date": "",
        "game_minute": 0,
        "is_goalie": False,
        "stats": {
            "goals": 0,
            "assists": 0,
            "passes_successful": 0,
            "passes_unsuccessful": 0,
            "steals": 0,
            "turnovers": 0,
            "shots_on_target": 0,
            "shots_off_target": 0,
            "fouls_won": 0,
            "fouls_committed": 0,
            "clearances": 0,
            "interceptions": 0,
            # ── Goalie stats ──
            "saves": 0,
            "goals_allowed": 0,
            "goalie_clearances": 0,
        },
        "event_log": [],
        "viewing_game": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def log_event(event_name, stat_key, delta=1):
    st.session_state.stats[stat_key] += delta
    minute = st.session_state.game_minute
    st.session_state.event_log.append({
        "event": event_name,
        "minute": minute,
        "time": datetime.now().strftime("%H:%M:%S")
    })

def undo_last():
    if not st.session_state.event_log:
        return
    last = st.session_state.event_log.pop()
    event_to_stat = {
        "⚽ Goal":                    "goals",
        "🎯 Assist":                  "assists",
        "✅ Successful Pass":          "passes_successful",
        "❌ Unsuccessful Pass":        "passes_unsuccessful",
        "🔵 Steal":                   "steals",
        "🔴 Turnover":                "turnovers",
        "🎯 Shot on Target":          "shots_on_target",
        "💨 Shot off Target":         "shots_off_target",
        "🏳️ Foul Won":               "fouls_won",
        "⚠️ Foul Committed":         "fouls_committed",
        "🛡️ Clearance":              "clearances",
        "✂️ Interception":           "interceptions",
        # Goalie
        "🧤 Save":                    "saves",
        "🚨 Goal Allowed":            "goals_allowed",
        "👊 Goalie Clearance":        "goalie_clearances",
    }
    key = event_to_stat.get(last["event"])
    if key and st.session_state.stats.get(key, 0) > 0:
        st.session_state.stats[key] -= 1

def pass_accuracy():
    total = st.session_state.stats["passes_successful"] + st.session_state.stats["passes_unsuccessful"]
    if total == 0:
        return 0, 0
    acc = st.session_state.stats["passes_successful"] / total * 100
    return round(acc, 1), total

def save_percentage():
    s = st.session_state.stats
    total_faced = s["saves"] + s["goals_allowed"]
    if total_faced == 0:
        return 0, 0
    pct = s["saves"] / total_faced * 100
    return round(pct, 1), total_faced

def save_current_game():
    data = load_data()
    game = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "player": st.session_state.player_name,
        "opponent": st.session_state.opponent,
        "date": st.session_state.game_date,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "is_goalie": st.session_state.is_goalie,
        "stats": dict(st.session_state.stats),
        "event_log": list(st.session_state.event_log),
    }
    data["games"].append(game)
    save_data(data)
    gh_ok, gh_msg = push_csv_to_github(data["games"])
    return game["id"], gh_ok, gh_msg

def reset_tracker():
    keys = ["player_name","opponent","game_date","game_minute","is_goalie","stats","event_log","viewing_game"]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    init_session()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
col_logo, col_nav = st.columns([3, 2])
with col_logo:
    st.markdown('<div class="app-title">⚽ SOCCER TRACKER</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-sub">Player Performance Dashboard</div>', unsafe_allow_html=True)
with col_nav:
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2, n3, n4 = st.columns(4)
with n1:
    if st.button("🏠 Home"):
        st.session_state.screen = "home"
        st.rerun()
with n2:
    if st.button("📋 History"):
        st.session_state.screen = "history"
        st.rerun()
with n3:
    if st.button("📈 Trends"):
        st.session_state.screen = "trends"
        st.rerun()
with n4:
    if st.session_state.screen == "tracking":
        if st.button("💾 Save Game"):
            gid, gh_ok, gh_msg = save_current_game()
            st.success("Game saved!")
            if gh_ok:
                st.success(gh_msg)
            else:
                st.warning(gh_msg)

st.markdown("<hr style='border:1px solid #1e3a23; margin: 0.5rem 0 1rem;'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN: HOME
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.screen == "home":
    st.markdown('<div class="section-label">New Game Setup</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        player = st.text_input("Player Name", value=st.session_state.player_name, placeholder="e.g. Alex Morgan")
    with col2:
        opponent = st.text_input("Opponent Team", value=st.session_state.opponent, placeholder="e.g. Red FC")
    with col3:
        date = st.date_input("Game Date", value=datetime.today())

    is_goalie = st.checkbox(
        "🧤 This player is a goalkeeper — enable goalie stats",
        value=st.session_state.is_goalie
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("▶️  Start Tracking", use_container_width=False):
        if player.strip():
            st.session_state.player_name = player.strip()
            st.session_state.opponent = opponent.strip() or "Unknown"
            st.session_state.game_date = str(date)
            st.session_state.is_goalie = is_goalie
            st.session_state.screen = "tracking"
            st.rerun()
        else:
            st.error("Please enter the player's name.")

    # Recent games preview
    data = load_data()
    if data["games"]:
        st.markdown('<div class="section-label">Recent Games</div>', unsafe_allow_html=True)
        for game in reversed(data["games"][-5:]):
            acc, total = 0, 0
            if game["stats"]["passes_successful"] + game["stats"]["passes_unsuccessful"] > 0:
                total = game["stats"]["passes_successful"] + game["stats"]["passes_unsuccessful"]
                acc = round(game["stats"]["passes_successful"] / total * 100, 1)

            goalie_badge = " 🧤" if game.get("is_goalie") else ""
            goalie_extra = ""
            if game.get("is_goalie"):
                gs = game["stats"]
                total_faced = gs.get("saves", 0) + gs.get("goals_allowed", 0)
                sv_pct = round(gs.get("saves", 0) / total_faced * 100, 1) if total_faced > 0 else 0
                goalie_extra = f"&nbsp;·&nbsp; 🧤 {gs.get('saves',0)} saves &nbsp;·&nbsp; SV% {sv_pct}%"

            st.markdown(f"""
            <div class="saved-game-row">
                <strong style="color:#e8f5e9;">{game['player']}{goalie_badge}</strong>
                vs {game['opponent']} &nbsp;·&nbsp;
                ⚽ {game['stats']['goals']} goals &nbsp;·&nbsp;
                🎯 {game['stats']['assists']} assists &nbsp;·&nbsp;
                Pass accuracy: {acc}% ({total} passes){goalie_extra}
                <div class="saved-game-date">{game['date']} · Saved {game['saved_at']}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN: TRACKING
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.screen == "tracking":
    s = st.session_state.stats
    acc, total_passes = pass_accuracy()
    sv_pct, total_faced = save_percentage()

    goalie_badge = " 🧤" if st.session_state.is_goalie else ""

    # Game header
    st.markdown(f"""
    <div class="game-card">
        <div class="game-title-text">{st.session_state.player_name}{goalie_badge}</div>
        <div class="game-meta">vs {st.session_state.opponent} &nbsp;·&nbsp; {st.session_state.game_date}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live stats row ────────────────────────────────────────────────
    st.markdown('<div class="section-label">Live Stats</div>', unsafe_allow_html=True)

    stat_cols = st.columns(6)
    live_stats = [
        ("⚽", str(s["goals"]),               "Goals",          ""),
        ("🎯", str(s["assists"]),              "Assists",        ""),
        ("✅", str(s["passes_successful"]),    "Good Passes",    ""),
        ("❌", str(s["passes_unsuccessful"]), "Bad Passes",     ""),
        ("🔵", str(s["steals"]),              "Steals",         ""),
        ("🔴", str(s["turnovers"]),            "Turnovers",      ""),
    ]
    for i, (icon, val, label, sub) in enumerate(live_stats):
        with stat_cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{val}</div>
                <div class="stat-label">{icon} {label}</div>
            </div>""", unsafe_allow_html=True)

    stat_cols2 = st.columns(6)
    live_stats2 = [
        ("🎯", str(s["shots_on_target"]),    "Shots On",     ""),
        ("💨", str(s["shots_off_target"]),   "Shots Off",    ""),
        ("🏳️", str(s["fouls_won"]),          "Fouls Won",    ""),
        ("⚠️", str(s["fouls_committed"]),   "Fouls Given",  ""),
        ("🛡️", str(s["clearances"]),        "Clearances",   ""),
        ("✂️", str(s["interceptions"]),     "Intercepts",   ""),
    ]
    for i, (icon, val, label, sub) in enumerate(live_stats2):
        with stat_cols2[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{val}</div>
                <div class="stat-label">{icon} {label}</div>
            </div>""", unsafe_allow_html=True)

    # ── Goalie live stats row ─────────────────────────────────────────
    if st.session_state.is_goalie:
        st.markdown('<div class="section-label" style="color:#a08030;">🧤 Goalie Stats</div>', unsafe_allow_html=True)
        gcols = st.columns(3)
        goalie_live = [
            ("🧤", str(s["saves"]),           "Saves"),
            ("🚨", str(s["goals_allowed"]),   "Goals Allowed"),
            ("👊", str(s["goalie_clearances"]),"Goalie Clearances"),
        ]
        for i, (icon, val, label) in enumerate(goalie_live):
            with gcols[i]:
                st.markdown(f"""
                <div class="stat-card-goalie">
                    <div class="stat-number-goalie">{val}</div>
                    <div class="stat-label-goalie">{icon} {label}</div>
                </div>""", unsafe_allow_html=True)

        # Save % bar
        bar_width = sv_pct if sv_pct > 0 else 0
        bar_color = "#ffc107" if sv_pct >= 70 else "#ff9800" if sv_pct >= 50 else "#f44336"
        st.markdown(f"""
        <div style="margin: 0.5rem 0 0.5rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:#a08030;">
                <span>Save Percentage</span>
                <span style="color:#ffe082; font-weight:600;">{sv_pct}%  ({total_faced} shots faced)</span>
            </div>
            <div class="save-bar-bg">
                <div class="save-bar-fill" style="width:{bar_width}%; background:{bar_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Pass accuracy bar
    bar_width = acc if acc > 0 else 0
    bar_color = "#4caf50" if acc >= 70 else "#ff9800" if acc >= 50 else "#f44336"
    st.markdown(f"""
    <div style="margin: 0.5rem 0 1rem;">
        <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:#6a9e6e;">
            <span>Pass Accuracy</span>
            <span style="color:#e8f5e9; font-weight:600;">{acc}%  ({total_passes} passes)</span>
        </div>
        <div class="accuracy-bar-bg">
            <div class="accuracy-bar-fill" style="width:{bar_width}%; background:{bar_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Game minute ───────────────────────────────────────────────────
    min_col1, min_col2 = st.columns([1, 4])
    with min_col1:
        st.session_state.game_minute = st.number_input(
            "Game Minute", min_value=0, max_value=120,
            value=st.session_state.game_minute, step=1,
            label_visibility="visible"
        )

    # ── Event buttons ─────────────────────────────────────────────────
    st.markdown('<div class="section-label">Log an Event</div>', unsafe_allow_html=True)

    # Attacking
    st.markdown('<div class="event-section">', unsafe_allow_html=True)
    st.markdown('<div class="event-section-title">⚔️ Attacking</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        if st.button("⚽  Goal"):
            log_event("⚽ Goal", "goals")
            st.rerun()
    with a2:
        if st.button("🎯  Assist"):
            log_event("🎯 Assist", "assists")
            st.rerun()
    with a3:
        if st.button("🎯  Shot on Target"):
            log_event("🎯 Shot on Target", "shots_on_target")
            st.rerun()
    with a4:
        if st.button("💨  Shot off Target"):
            log_event("💨 Shot off Target", "shots_off_target")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Passing
    st.markdown('<div class="event-section">', unsafe_allow_html=True)
    st.markdown('<div class="event-section-title">🔄 Passing</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        if st.button("✅  Successful Pass"):
            log_event("✅ Successful Pass", "passes_successful")
            st.rerun()
    with p2:
        if st.button("❌  Unsuccessful Pass"):
            log_event("❌ Unsuccessful Pass", "passes_unsuccessful")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Defensive
    st.markdown('<div class="event-section">', unsafe_allow_html=True)
    st.markdown('<div class="event-section-title">🛡️ Defensive</div>', unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        if st.button("🔵  Steal"):
            log_event("🔵 Steal", "steals")
            st.rerun()
    with d2:
        if st.button("✂️  Interception"):
            log_event("✂️ Interception", "interceptions")
            st.rerun()
    with d3:
        if st.button("🛡️  Clearance"):
            log_event("🛡️ Clearance", "clearances")
            st.rerun()
    with d4:
        if st.button("🏳️  Foul Won"):
            log_event("🏳️ Foul Won", "fouls_won")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Negative events
    st.markdown('<div class="event-section">', unsafe_allow_html=True)
    st.markdown('<div class="event-section-title">⚠️ Negative Events</div>', unsafe_allow_html=True)
    n1, n2 = st.columns(2)
    with n1:
        if st.button("🔴  Turnover"):
            log_event("🔴 Turnover", "turnovers")
            st.rerun()
    with n2:
        if st.button("⚠️  Foul Committed"):
            log_event("⚠️ Foul Committed", "fouls_committed")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Goalie event buttons ──────────────────────────────────────────
    if st.session_state.is_goalie:
        st.markdown('<div class="event-section-goalie">', unsafe_allow_html=True)
        st.markdown('<div class="event-section-title-goalie">🧤 Goalkeeper Events</div>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            if st.button("🧤  Save"):
                log_event("🧤 Save", "saves")
                st.rerun()
        with g2:
            if st.button("🚨  Goal Allowed"):
                log_event("🚨 Goal Allowed", "goals_allowed")
                st.rerun()
        with g3:
            if st.button("👊  Goalie Clearance"):
                log_event("👊 Goalie Clearance", "goalie_clearances")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Undo + Save ───────────────────────────────────────────────────
    undo_col, save_col, end_col = st.columns([1, 1, 1])
    with undo_col:
        if st.button("↩️  Undo Last Event"):
            undo_last()
            st.rerun()
    with save_col:
        if st.button("💾  Save Game"):
            _, gh_ok, gh_msg = save_current_game()
            if gh_ok:
                st.success(f"✅ Game saved! {gh_msg}")
            else:
                st.success("✅ Game saved locally.")
                st.warning(gh_msg)
            st.rerun()
    with end_col:
        if st.button("🏁  End & Save Game"):
            _, gh_ok, gh_msg = save_current_game()
            reset_tracker()
            st.session_state.screen = "history"
            if not gh_ok:
                st.session_state["_gh_warn"] = gh_msg
            st.rerun()

    # ── Event log ─────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Event Log</div>', unsafe_allow_html=True)
    if st.session_state.event_log:
        for entry in reversed(st.session_state.event_log[-20:]):
            st.markdown(f"""
            <div class="log-entry">
                <span>{entry['event']}</span>
                <span class="log-time">⏱ {entry['minute']}' &nbsp; {entry['time']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#3a6b3e; font-size:0.85rem;">No events logged yet — start tracking!</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN: HISTORY
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.screen == "history":
    st.markdown('<div class="section-label">Game History</div>', unsafe_allow_html=True)

    # Show deferred GitHub push warning from End & Save
    if st.session_state.get("_gh_warn"):
        st.warning(st.session_state.pop("_gh_warn"))

    data = load_data()

    if not data["games"]:
        st.markdown('<div style="color:#3a6b3e; font-size:0.9rem;">No games saved yet. Start tracking a game!</div>', unsafe_allow_html=True)
    else:
        for game in reversed(data["games"]):
            s = game["stats"]
            total = s["passes_successful"] + s["passes_unsuccessful"]
            acc = round(s["passes_successful"] / total * 100, 1) if total > 0 else 0

            goalie_badge = " 🧤" if game.get("is_goalie") else ""
            with st.expander(f"⚽ {game['player']}{goalie_badge} vs {game['opponent']} — {game['date']}"):
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                with c1:
                    st.metric("Goals", s["goals"])
                with c2:
                    st.metric("Assists", s["assists"])
                with c3:
                    st.metric("Pass Acc.", f"{acc}%")
                with c4:
                    st.metric("Steals", s["steals"])
                with c5:
                    st.metric("Turnovers", s["turnovers"])
                with c6:
                    st.metric("Interceptions", s["interceptions"])

                c7, c8, c9, c10, c11, c12 = st.columns(6)
                with c7:
                    st.metric("Shots On", s["shots_on_target"])
                with c8:
                    st.metric("Shots Off", s["shots_off_target"])
                with c9:
                    st.metric("Good Passes", s["passes_successful"])
                with c10:
                    st.metric("Bad Passes", s["passes_unsuccessful"])
                with c11:
                    st.metric("Fouls Won", s["fouls_won"])
                with c12:
                    st.metric("Fouls Given", s["fouls_committed"])

                # ── Goalie stats in history ───────────────────────────
                if game.get("is_goalie"):
                    st.markdown("---")
                    st.markdown("**🧤 Goalkeeper Stats**")
                    saves = s.get("saves", 0)
                    goals_allowed = s.get("goals_allowed", 0)
                    goalie_clearances = s.get("goalie_clearances", 0)
                    total_faced = saves + goals_allowed
                    sv_pct = round(saves / total_faced * 100, 1) if total_faced > 0 else 0

                    gc1, gc2, gc3, gc4 = st.columns(4)
                    with gc1:
                        st.metric("Saves", saves)
                    with gc2:
                        st.metric("Goals Allowed", goals_allowed)
                    with gc3:
                        st.metric("Goalie Clearances", goalie_clearances)
                    with gc4:
                        st.metric("Save %", f"{sv_pct}%")

                # Event log
                if game.get("event_log"):
                    st.markdown("**Event Timeline:**")
                    for entry in game["event_log"]:
                        st.markdown(f"""
                        <div class="log-entry">
                            <span>{entry['event']}</span>
                            <span class="log-time">⏱ {entry['minute']}'</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Delete button
                if st.button(f"🗑️ Delete this game", key=f"del_{game['id']}"):
                    data["games"] = [g for g in data["games"] if g["id"] != game["id"]]
                    save_data(data)
                    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN: TRENDS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.screen == "trends":
    import pandas as pd

    st.markdown('<div class="section-label">Player Trends</div>', unsafe_allow_html=True)

    data = load_data()

    if not data["games"]:
        st.markdown('<div style="color:#3a6b3e; font-size:0.9rem;">No games saved yet. Track some games first!</div>', unsafe_allow_html=True)
    else:
        players = sorted(set(g["player"] for g in data["games"]))
        selected_player = st.selectbox("Select Player", players)

        player_games = sorted(
            [g for g in data["games"] if g["player"] == selected_player],
            key=lambda g: g["date"]
        )

        is_goalie_player = any(g.get("is_goalie") for g in player_games)

        if len(player_games) < 1:
            st.info("No games found for this player.")
        else:
            rows = []
            for g in player_games:
                s = g["stats"]
                total_passes = s["passes_successful"] + s["passes_unsuccessful"]
                acc = round(s["passes_successful"] / total_passes * 100, 1) if total_passes > 0 else 0
                total_shots = s["shots_on_target"] + s["shots_off_target"]
                shot_acc = round(s["shots_on_target"] / total_shots * 100, 1) if total_shots > 0 else 0
                saves = s.get("saves", 0)
                goals_allowed = s.get("goals_allowed", 0)
                goalie_clearances = s.get("goalie_clearances", 0)
                total_faced = saves + goals_allowed
                sv_pct = round(saves / total_faced * 100, 1) if total_faced > 0 else 0
                rows.append({
                    "Date": g["date"],
                    "Opponent": g["opponent"],
                    "Goals": s["goals"],
                    "Assists": s["assists"],
                    "Goal Contributions": s["goals"] + s["assists"],
                    "Successful Passes": s["passes_successful"],
                    "Unsuccessful Passes": s["passes_unsuccessful"],
                    "Total Passes": total_passes,
                    "Pass Accuracy %": acc,
                    "Shots on Target": s["shots_on_target"],
                    "Shots off Target": s["shots_off_target"],
                    "Total Shots": total_shots,
                    "Shot Accuracy %": shot_acc,
                    "Steals": s["steals"],
                    "Interceptions": s["interceptions"],
                    "Clearances": s["clearances"],
                    "Turnovers": s["turnovers"],
                    "Fouls Won": s["fouls_won"],
                    "Fouls Committed": s["fouls_committed"],
                    # Goalie
                    "Saves": saves,
                    "Goals Allowed": goals_allowed,
                    "Goalie Clearances": goalie_clearances,
                    "Save %": sv_pct,
                    "Shots Faced": total_faced,
                })

            df = pd.DataFrame(rows)

            # ── Career summary cards ──────────────────────────────────
            st.markdown('<div class="section-label">Career Averages</div>', unsafe_allow_html=True)

            avg = df.mean(numeric_only=True)
            total = df.sum(numeric_only=True)
            games_played = len(df)

            s1, s2, s3, s4, s5, s6 = st.columns(6)
            with s1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{int(total['Goals'])}</div>
                    <div class="stat-label">⚽ Total Goals</div>
                    <div class="stat-sub">{avg['Goals']:.1f} per game</div>
                </div>""", unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{int(total['Assists'])}</div>
                    <div class="stat-label">🎯 Total Assists</div>
                    <div class="stat-sub">{avg['Assists']:.1f} per game</div>
                </div>""", unsafe_allow_html=True)
            with s3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{avg['Pass Accuracy %']:.1f}%</div>
                    <div class="stat-label">✅ Avg Pass Acc.</div>
                    <div class="stat-sub">{int(total['Total Passes'])} total passes</div>
                </div>""", unsafe_allow_html=True)
            with s4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{int(total['Steals'])}</div>
                    <div class="stat-label">🔵 Total Steals</div>
                    <div class="stat-sub">{avg['Steals']:.1f} per game</div>
                </div>""", unsafe_allow_html=True)
            with s5:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{int(total['Turnovers'])}</div>
                    <div class="stat-label">🔴 Total Turnovers</div>
                    <div class="stat-sub">{avg['Turnovers']:.1f} per game</div>
                </div>""", unsafe_allow_html=True)
            with s6:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{games_played}</div>
                    <div class="stat-label">📋 Games Played</div>
                    <div class="stat-sub">all time</div>
                </div>""", unsafe_allow_html=True)

            # ── Goalie career summary ─────────────────────────────────
            if is_goalie_player:
                st.markdown('<div class="section-label" style="color:#a08030;">🧤 Goalkeeper Career Averages</div>', unsafe_allow_html=True)
                total_saves = int(total["Saves"])
                total_allowed = int(total["Goals Allowed"])
                total_gk_clears = int(total["Goalie Clearances"])
                total_faced_all = total_saves + total_allowed
                career_sv_pct = round(total_saves / total_faced_all * 100, 1) if total_faced_all > 0 else 0

                gk1, gk2, gk3, gk4 = st.columns(4)
                with gk1:
                    st.markdown(f"""
                    <div class="stat-card-goalie">
                        <div class="stat-number-goalie">{total_saves}</div>
                        <div class="stat-label-goalie">🧤 Total Saves</div>
                    </div>""", unsafe_allow_html=True)
                with gk2:
                    st.markdown(f"""
                    <div class="stat-card-goalie">
                        <div class="stat-number-goalie">{total_allowed}</div>
                        <div class="stat-label-goalie">🚨 Goals Allowed</div>
                    </div>""", unsafe_allow_html=True)
                with gk3:
                    st.markdown(f"""
                    <div class="stat-card-goalie">
                        <div class="stat-number-goalie">{total_gk_clears}</div>
                        <div class="stat-label-goalie">👊 Goalie Clearances</div>
                    </div>""", unsafe_allow_html=True)
                with gk4:
                    st.markdown(f"""
                    <div class="stat-card-goalie">
                        <div class="stat-number-goalie">{career_sv_pct}%</div>
                        <div class="stat-label-goalie">📊 Career Save %</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Stat selector for chart ───────────────────────────────
            st.markdown('<div class="section-label">Game-by-Game Trend</div>', unsafe_allow_html=True)

            STAT_OPTIONS = [
                "Goals", "Assists", "Goal Contributions",
                "Pass Accuracy %", "Total Passes", "Successful Passes", "Unsuccessful Passes",
                "Shots on Target", "Total Shots", "Shot Accuracy %",
                "Steals", "Interceptions", "Clearances", "Turnovers",
                "Fouls Won", "Fouls Committed",
            ]

            if is_goalie_player:
                STAT_OPTIONS += ["Saves", "Goals Allowed", "Goalie Clearances", "Save %", "Shots Faced"]

            col_stat, col_chart_type = st.columns([3, 1])
            with col_stat:
                selected_stats = st.multiselect(
                    "Choose stats to compare",
                    options=STAT_OPTIONS,
                    default=["Goals", "Assists", "Pass Accuracy %"]
                )
            with col_chart_type:
                chart_type = st.selectbox("Chart type", ["Line", "Bar"])

            if selected_stats:
                chart_df = df[["Date"] + selected_stats].set_index("Date")
                if chart_type == "Line":
                    st.line_chart(chart_df, use_container_width=True, height=350)
                else:
                    st.bar_chart(chart_df, use_container_width=True, height=350)
            else:
                st.info("Select at least one stat above to see the chart.")

            # ── Game by game table ────────────────────────────────────
            st.markdown('<div class="section-label">Full Game Log</div>', unsafe_allow_html=True)

            display_cols = ["Date", "Opponent", "Goals", "Assists",
                            "Pass Accuracy %", "Total Passes", "Steals",
                            "Turnovers", "Interceptions", "Shots on Target"]
            if is_goalie_player:
                display_cols += ["Saves", "Goals Allowed", "Save %"]

            st.dataframe(
                df[display_cols].style.format({
                    "Pass Accuracy %": "{:.1f}%",
                    "Shot Accuracy %": "{:.1f}%",
                    "Save %": "{:.1f}%",
                }),
                use_container_width=True,
                hide_index=True
            )

            # ── Best/worst game highlights ────────────────────────────
            if len(df) > 1:
                st.markdown('<div class="section-label">Highlights</div>', unsafe_allow_html=True)

                highlight_cols = 4 if is_goalie_player else 3
                h_cols = st.columns(highlight_cols)

                best_goals_idx  = df["Goals"].idxmax()
                best_pass_idx   = df["Pass Accuracy %"].idxmax()
                best_steals_idx = df["Steals"].idxmax()

                with h_cols[0]:
                    bg = df.loc[best_goals_idx]
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">⚽ {int(bg['Goals'])}</div>
                        <div class="stat-label">Best Goals Game</div>
                        <div class="stat-sub">vs {bg['Opponent']} · {bg['Date']}</div>
                    </div>""", unsafe_allow_html=True)
                with h_cols[1]:
                    bp = df.loc[best_pass_idx]
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">✅ {bp['Pass Accuracy %']:.0f}%</div>
                        <div class="stat-label">Best Pass Accuracy</div>
                        <div class="stat-sub">vs {bp['Opponent']} · {bp['Date']}</div>
                    </div>""", unsafe_allow_html=True)
                with h_cols[2]:
                    bs = df.loc[best_steals_idx]
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">🔵 {int(bs['Steals'])}</div>
                        <div class="stat-label">Most Steals Game</div>
                        <div class="stat-sub">vs {bs['Opponent']} · {bs['Date']}</div>
                    </div>""", unsafe_allow_html=True)

                if is_goalie_player and df["Shots Faced"].max() > 0:
                    best_sv_idx = df["Save %"].idxmax()
                    with h_cols[3]:
                        bsv = df.loc[best_sv_idx]
                        st.markdown(f"""
                        <div class="stat-card-goalie">
                            <div class="stat-number-goalie">🧤 {bsv['Save %']:.0f}%</div>
                            <div class="stat-label-goalie">Best Save %</div>
                            <div class="stat-sub" style="color:#a08030;">vs {bsv['Opponent']} · {bsv['Date']}</div>
                        </div>""", unsafe_allow_html=True)
