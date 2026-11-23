"""
NEXOR - Motivo-Inspired Design System & Stylesheet
A serene, luminous, modern enterprise AI SaaS design system.
Features a refined mint/teal palette, editorial typography, pristine cards,
pill buttons, and high-contrast accessible visual hierarchy.
"""

def get_css() -> str:
    """Return custom CSS styles for NEXOR Motivo-inspired UI."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=Newsreader:ital,opsz,wght@1,6..72,400;1,6..72,500;1,6..72,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* =========================================================
       CSS VARIABLES & MOTIVO PALETTE
       ========================================================= */
    :root {
        --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --font-serif-italic: 'Newsreader', Georgia, serif;
        --font-mono: 'JetBrains Mono', monospace;

        /* Motivo Luminous Palette */
        --bg-app: #F7FAF9;
        --bg-card: #FFFFFF;
        --bg-mint-soft: #E8F5F1;
        --bg-mint-subtle: #F0FAF6;
        --bg-sky-soft: #E0F2FE;
        --bg-teal-dark: #13635B;
        --bg-teal-darker: #0D4943;
        --bg-obsidian: #11181C;
        --bg-obsidian-hover: #222D33;

        /* Text colors - Guaranteed High Contrast */
        --text-headline: #11181C;
        --text-body: #2C3E42;
        --text-muted: #5F7377;
        --text-teal: #0D7B70;
        --text-white: #FFFFFF;

        /* Borders & Lines */
        --border-light: #E4ECE9;
        --border-mint: #C4EADF;
        --border-teal: #0D9488;
        --border-focus: #14B8A6;

        /* Radii */
        --radius-pill: 9999px;
        --radius-card: 20px;
        --radius-sm: 10px;
        --radius-md: 14px;
    }

    /* =========================================================
       HEADER & SIDEBAR COLLAPSE / EXPAND TOGGLE CONTROLS
       ========================================================= */
    header[data-testid="stHeader"],
    .stAppHeader {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        pointer-events: none !important;
        height: 3.5rem !important;
        z-index: 9999 !important;
    }

    div[data-testid="stToolbar"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        pointer-events: none !important;
        display: flex !important;
        visibility: visible !important;
    }

    [data-testid="stAppDeployButton"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    /* Open/Expand sidebar button (visible at top left when sidebar is closed) */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    button[aria-label="Expand sidebar"] {
        display: inline-flex !important;
        visibility: visible !important;
        pointer-events: auto !important;
        opacity: 1 !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E4ECE9 !important;
        border-radius: 10px !important;
        padding: 6px 10px !important;
        box-shadow: 0 2px 8px rgba(17, 24, 28, 0.08) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin-left: 12px !important;
        margin-top: 8px !important;
        z-index: 100000 !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    button[aria-label="Expand sidebar"]:hover {
        background-color: #F0FAF6 !important;
        border-color: #0D7B70 !important;
        transform: scale(1.05);
    }

    [data-testid="stExpandSidebarButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {
        color: #11181C !important;
    }

    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    button[aria-label="Expand sidebar"] svg {
        fill: #11181C !important;
        stroke: #11181C !important;
    }

    /* Close sidebar button (inside sidebar when open) */
    [data-testid="stSidebarCollapseButton"],
    button[aria-label="Collapse sidebar"] {
        display: inline-flex !important;
        visibility: visible !important;
        pointer-events: auto !important;
        opacity: 1 !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E4ECE9 !important;
        border-radius: 10px !important;
        color: #11181C !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    button[aria-label="Collapse sidebar"] svg {
        fill: #11181C !important;
        stroke: #11181C !important;
    }

    /* =========================================================
       GLOBAL APP BASE
       ========================================================= */
    html, body, [class*="css"] {
        font-family: var(--font-sans) !important;
        color: var(--text-headline) !important;
        background-color: var(--bg-app) !important;
    }

    .stApp {
        background-color: var(--bg-app) !important;
        color: var(--text-headline) !important;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* =========================================================
       SIDEBAR NAVIGATION
       ========================================================= */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--border-light) !important;
        box-shadow: 2px 0 16px rgba(17, 24, 28, 0.03) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-headline) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--text-muted) !important;
        font-size: 0.85rem;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 10px 14px !important;
        border-radius: var(--radius-sm) !important;
        transition: all 0.2s ease !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
        color: var(--text-headline) !important;
        background: transparent !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: var(--bg-mint-subtle) !important;
        color: var(--text-teal) !important;
        border-color: var(--border-mint) !important;
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"],
    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: var(--bg-mint-soft) !important;
        color: var(--text-teal) !important;
        border: 1px solid var(--border-mint) !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: var(--border-light) !important;
        margin: 1.25rem 0 !important;
    }

    /* =========================================================
       TYPOGRAPHY
       ========================================================= */
    .serif-italic {
        font-family: var(--font-serif-italic) !important;
        font-style: italic !important;
        font-weight: 500 !important;
        color: var(--text-teal) !important;
        letter-spacing: -0.01em;
    }

    .motivo-headline {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.15;
        color: var(--text-headline);
        margin: 0 0 1rem 0;
    }

    .motivo-subheadline {
        font-size: 1.05rem;
        color: var(--text-muted);
        line-height: 1.6;
        max-width: 620px;
        margin: 0 0 1.5rem 0;
    }

    /* =========================================================
       BUTTONS
       ========================================================= */
    div.stButton > button {
        border-radius: var(--radius-pill) !important;
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1px solid transparent !important;
        box-shadow: 0 1px 3px rgba(17, 24, 28, 0.05) !important;
        cursor: pointer !important;
    }

    /* Primary Dark Obsidian Pill */
    div.stButton > button[kind="primary"] {
        background-color: var(--bg-obsidian) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--bg-obsidian) !important;
        box-shadow: 0 2px 8px rgba(17, 24, 28, 0.18) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: var(--bg-obsidian-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(17, 24, 28, 0.25) !important;
    }

    /* Secondary White/Outline Pill */
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: var(--text-headline) !important;
        border: 1.5px solid var(--border-light) !important;
    }

    div.stButton > button[kind="secondary"]:hover {
        background-color: var(--bg-mint-subtle) !important;
        border-color: var(--border-mint) !important;
        color: var(--text-teal) !important;
        transform: translateY(-1px);
    }

    /* =========================================================
       CARD CONTAINERS & METRICS
       ========================================================= */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-card) !important;
        box-shadow: 0 4px 20px -2px rgba(13, 123, 112, 0.06) !important;
        padding: 0.75rem !important;
        margin-bottom: 1.25rem !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 1.25rem 1.4rem !important;
        border-radius: var(--radius-card) !important;
        border: 1px solid var(--border-light) !important;
        box-shadow: 0 1px 3px rgba(17, 24, 28, 0.04) !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-headline) !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
    }

    /* =========================================================
       FORM CONTROLS - GUARANTEED LIGHT THEME & READABILITY
       ========================================================= */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #11181C !important;
        border: 1.5px solid var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-sans) !important;
        font-size: 0.92rem !important;
    }

    /* Selectboxes: BaseWeb overrides for pure white surface */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #11181C !important;
        border: 1.5px solid var(--border-light) !important;
        border-radius: var(--radius-sm) !important;
    }

    div[data-baseweb="select"] * {
        color: #11181C !important;
    }

    div[data-baseweb="popover"],
    ul[role="listbox"],
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #11181C !important;
    }

    li[role="option"]:hover {
        background-color: var(--bg-mint-soft) !important;
        color: var(--text-teal) !important;
    }

    /* Radio buttons high-contrast text */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label div,
    div[data-testid="stRadio"] * {
        color: #11181C !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* =========================================================
       FILE UPLOADER - CLEAN MINT/WHITE DROPZONE (NO BLACK TUBE)
       ========================================================= */
    div[data-testid="stFileUploader"] {
        background: transparent !important;
    }

    div[data-testid="stFileUploader"] section {
        background-color: #F0FAF6 !important;
        border: 2px dashed #0D7B70 !important;
        border-radius: var(--radius-card) !important;
        padding: 2rem !important;
        text-align: center !important;
    }

    div[data-testid="stFileUploader"] section > div,
    div[data-testid="stFileUploader"] section p,
    div[data-testid="stFileUploader"] section span:not(button span),
    div[data-testid="stFileUploaderDropzoneInstructions"] {
        color: #11181C !important;
        font-weight: 600 !important;
    }

    div[data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #5F7377 !important;
        font-weight: 500 !important;
    }

    /* Black box button displaying 'Upload here' */
    div[data-testid="stFileUploader"] button {
        background-color: #11181C !important;
        color: #FFFFFF !important;
        border-radius: var(--radius-pill) !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.6rem !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 120px !important;
    }

    div[data-testid="stFileUploader"] button::after {
        content: "Upload here" !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        display: inline-block !important;
        font-family: var(--font-sans) !important;
        visibility: visible !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background-color: #222D33 !important;
    }

    div[data-testid="stFileUploader"] button * {
        display: none !important;
    }

    /* =========================================================
       INTERACTIVE CHAT INPUT (NO BLACK FOOTER)
       ========================================================= */
    div[data-testid="stBottom"] {
        background-color: transparent !important;
        border-top: none !important;
    }

    div[data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 2px solid #0D7B70 !important;
        border-radius: var(--radius-pill) !important;
        box-shadow: 0 4px 20px rgba(13, 123, 112, 0.12) !important;
        padding: 6px 14px !important;
        margin-bottom: 1rem !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #044E46 !important;
        box-shadow: 0 6px 25px rgba(13, 123, 112, 0.22) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #11181C !important;
        background-color: transparent !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #5F7377 !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: #0D7B70 !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
    }

    div[data-testid="stChatInput"] button svg {
        fill: #FFFFFF !important;
    }

    /* =========================================================
       MOTIVO CARDS & BADGES
       ========================================================= */
    .motivo-pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--bg-mint-soft);
        color: var(--text-teal);
        border: 1px solid var(--border-mint);
        border-radius: var(--radius-pill);
        padding: 5px 14px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 1.25rem;
    }

    .motivo-pill-badge .badge-tag {
        background: #FFFFFF;
        color: var(--text-teal);
        padding: 2px 7px;
        border-radius: var(--radius-pill);
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .motivo-metrics-ribbon {
        background: #FFFFFF;
        border: 1px solid var(--border-light);
        border-radius: var(--radius-card);
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(13, 123, 112, 0.06);
        margin: 1.5rem 0 2rem 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.5rem;
    }

    .ribbon-item {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .ribbon-icon-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
    }

    .ribbon-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--text-headline);
        line-height: 1.1;
    }

    .ribbon-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        font-weight: 600;
        margin-top: 2px;
    }

    .motivo-deep-teal-card {
        background: linear-gradient(135deg, #13635B 0%, #0D4943 100%);
        border-radius: var(--radius-card);
        padding: 2rem 2.25rem;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px -4px rgba(19, 99, 91, 0.25);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .motivo-deep-teal-card * {
        color: #FFFFFF !important;
    }

    /* Badges */
    .badge-mint {
        background-color: var(--bg-mint-soft);
        color: var(--text-teal);
        border: 1px solid var(--border-mint);
        padding: 4px 10px;
        border-radius: var(--radius-pill);
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1;
    }

    .badge-pdf {
        background-color: #FFE4E6;
        color: #BE123C;
        border: 1px solid #FECDD3;
        font-weight: 700;
        font-family: var(--font-mono);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }

    .badge-docx {
        background-color: #DBEAFE;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        font-weight: 700;
        font-family: var(--font-mono);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }

    .badge-txt {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
        font-weight: 700;
        font-family: var(--font-mono);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }

    /* Live Pulsing Dot */
    .pulse-dot-green {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulseGreen 2s infinite;
        vertical-align: middle;
        margin-right: 6px;
    }

    .pulse-dot-red {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #EF4444;
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
        animation: pulseGreen 2s infinite;
        vertical-align: middle;
        margin-right: 6px;
    }

    @keyframes pulseGreen {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Source Box */
    .source-box {
        background: #FFFFFF;
        border: 1px solid var(--border-light);
        border-radius: var(--radius-sm);
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    .source-box-text {
        font-size: 0.86rem;
        color: var(--text-body);
        line-height: 1.5;
        background: var(--bg-mint-subtle);
        padding: 10px 12px;
        border-radius: 8px;
        border-left: 3px solid var(--text-teal);
        margin: 0;
    }

    /* Motivo Custom Data Table */
    .motivo-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #FFFFFF;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-light);
        overflow: hidden;
    }

    .motivo-table th {
        background-color: #F0FAF6;
        color: #11181C;
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-light);
        text-align: left;
    }

    .motivo-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #F0F4F2;
        color: #11181C;
        font-size: 0.88rem;
    }

    .motivo-table tr:last-child td {
        border-bottom: none;
    }

    .motivo-table tr:hover td {
        background-color: #F8FCFA;
    }
    </style>
    """
