import ctypes
import json
import os
import random
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

import keyboard
import pydirectinput
import win32con
import win32gui

APP_NAME = "Best BongoCat Clicker (BBC)"
EXE_NAME = "BBC"
CREATOR = "Nuunez"
CONFIG_DIR = Path(os.getenv("APPDATA", Path.home())) / "BBC"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "language": "auto",
    "theme": "default",
    "toggle_key": "f8",
    "window_title": "BongoCat",
    "interval_min_ms": 20,
    "interval_max_ms": 30,
    "hold_min_ms": 30,
    "hold_max_ms": 40,
    "actions": ["a", "s", "d"],
    "stop_when_focus_lost": True,
    "always_on_top": True,
}

TRANSLATIONS = {
    "en": {
        "settings": "Settings",
        "status_stopped": "● Stopped",
        "status_running": "● Running",
        "status_not_found": "BongoCat window not found",
        "status_focus": "Stopped: BongoCat lost focus",
        "status_error": "Stopped: input error",
        "status_hotkey_error": "Could not register toggle key",
        "start": "▶ Start",
        "stop": "■ Stop",
        "toggle": "Toggle key",
        "language": "Language",
        "theme": "Theme",
        "default": "Default",
        "dark": "Dark",
        "light": "Light",
        "auto": "Automatic (PC)",
        "actions": "Actions to execute",
        "actions_hint": "Use commas: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Delay between actions (ms)",
        "hold": "Key/click hold time (ms)",
        "min": "Min",
        "max": "Max",
        "window": "BongoCat window title",
        "find_window": "Select window",
        "window_help": "Choose the window BBC should control. Default: BongoCat.",
        "focus": "Stop if BongoCat loses focus",
        "topmost": "Keep BBC on top",
        "save": "Save",
        "cancel": "Cancel",
        "saved": "Settings saved.",
        "invalid": "Please enter valid values.",
        "invalid_actions": "Add at least one action.",
        "title": APP_NAME,
        "hint": "BBC only sends actions while the selected BongoCat window is active.",
        "version": "Version 1.0.0",
        "creator": "Created by Nuunez",
        "select_title": "Select BongoCat window",
        "select_hint": "Select the window BBC should control:",
        "refresh": "Refresh",
        "use_selected": "Use selected",
    },
    "pt": {
        "settings": "Definições",
        "status_stopped": "● Parado",
        "status_running": "● A funcionar",
        "status_not_found": "Janela do BongoCat não encontrada",
        "status_focus": "Parado: o BongoCat perdeu o foco",
        "status_error": "Parado: erro de entrada",
        "status_hotkey_error": "Não foi possível registar a tecla de toggle",
        "start": "▶ Iniciar",
        "stop": "■ Parar",
        "toggle": "Tecla de toggle",
        "language": "Idioma",
        "theme": "Tema",
        "default": "Predefinido",
        "dark": "Escuro",
        "light": "Claro",
        "auto": "Automático (PC)",
        "actions": "Ações a executar",
        "actions_hint": "Usa vírgulas: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Intervalo entre ações (ms)",
        "hold": "Tempo de pressão (ms)",
        "min": "Mín.",
        "max": "Máx.",
        "window": "Título da janela do BongoCat",
        "find_window": "Selecionar janela",
        "window_help": "Escolhe a janela que o BBC deve controlar. Predefinido: BongoCat.",
        "focus": "Parar se o BongoCat perder o foco",
        "topmost": "Manter o BBC no topo",
        "save": "Guardar",
        "cancel": "Cancelar",
        "saved": "Definições guardadas.",
        "invalid": "Introduz valores válidos.",
        "invalid_actions": "Adiciona pelo menos uma ação.",
        "title": APP_NAME,
        "hint": "O BBC só envia ações enquanto a janela selecionada do BongoCat estiver ativa.",
        "version": "Versão 1.0.0",
        "creator": "Criado por Nuunez",
        "select_title": "Selecionar janela do BongoCat",
        "select_hint": "Seleciona a janela que o BBC deve controlar:",
        "refresh": "Atualizar",
        "use_selected": "Usar selecionada",
    },
    "es": {
        "settings": "Configuración", "status_stopped": "● Detenido", "status_running": "● En ejecución",
        "status_not_found": "No se encontró la ventana de BongoCat", "status_focus": "Detenido: BongoCat perdió el foco",
        "status_error": "Detenido: error de entrada", "status_hotkey_error": "No se pudo registrar la tecla de activación",
        "start": "▶ Iniciar", "stop": "■ Detener", "toggle": "Tecla de activación", "language": "Idioma",
        "theme": "Tema", "default": "Predeterminado", "dark": "Oscuro", "light": "Claro", "auto": "Automático (PC)",
        "actions": "Acciones a ejecutar", "actions_hint": "Usa comas: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Intervalo entre acciones (ms)", "hold": "Tiempo de pulsación (ms)", "min": "Mín.", "max": "Máx.",
        "window": "Título de la ventana de BongoCat", "find_window": "Seleccionar ventana",
        "window_help": "Elige la ventana que BBC debe controlar. Predeterminado: BongoCat.",
        "focus": "Detener si BongoCat pierde el foco", "topmost": "Mantener BBC encima", "save": "Guardar", "cancel": "Cancelar",
        "saved": "Configuración guardada.", "invalid": "Introduce valores válidos.", "invalid_actions": "Añade al menos una acción.",
        "title": APP_NAME, "hint": "BBC solo envía acciones mientras la ventana seleccionada de BongoCat está activa.",
        "version": "Versión 1.0.0", "creator": "Creado por Nuunez", "select_title": "Seleccionar ventana de BongoCat",
        "select_hint": "Selecciona la ventana que BBC debe controlar:", "refresh": "Actualizar", "use_selected": "Usar seleccionada",
    },
    "fr": {
        "settings": "Paramètres", "status_stopped": "● Arrêté", "status_running": "● En cours",
        "status_not_found": "Fenêtre BongoCat introuvable", "status_focus": "Arrêté : BongoCat a perdu le focus",
        "status_error": "Arrêté : erreur d'entrée", "status_hotkey_error": "Impossible d'enregistrer la touche",
        "start": "▶ Démarrer", "stop": "■ Arrêter", "toggle": "Touche d'activation", "language": "Langue",
        "theme": "Thème", "default": "Par défaut", "dark": "Sombre", "light": "Clair", "auto": "Automatique (PC)",
        "actions": "Actions à exécuter", "actions_hint": "Utilisez des virgules : a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Délai entre les actions (ms)", "hold": "Durée de pression (ms)", "min": "Min.", "max": "Max.",
        "window": "Titre de la fenêtre BongoCat", "find_window": "Sélectionner la fenêtre",
        "window_help": "Choisissez la fenêtre que BBC doit contrôler. Par défaut : BongoCat.",
        "focus": "Arrêter si BongoCat perd le focus", "topmost": "Garder BBC au premier plan", "save": "Enregistrer", "cancel": "Annuler",
        "saved": "Paramètres enregistrés.", "invalid": "Saisissez des valeurs valides.", "invalid_actions": "Ajoutez au moins une action.",
        "title": APP_NAME, "hint": "BBC n'envoie des actions que lorsque la fenêtre BongoCat sélectionnée est active.",
        "version": "Version 1.0.0", "creator": "Créé par Nuunez", "select_title": "Sélectionner la fenêtre BongoCat",
        "select_hint": "Sélectionnez la fenêtre que BBC doit contrôler :", "refresh": "Actualiser", "use_selected": "Utiliser la sélection",
    },
    "de": {
        "settings": "Einstellungen", "status_stopped": "● Gestoppt", "status_running": "● Läuft",
        "status_not_found": "BongoCat-Fenster nicht gefunden", "status_focus": "Gestoppt: BongoCat hat den Fokus verloren",
        "status_error": "Gestoppt: Eingabefehler", "status_hotkey_error": "Aktivierungstaste konnte nicht registriert werden",
        "start": "▶ Start", "stop": "■ Stopp", "toggle": "Aktivierungstaste", "language": "Sprache",
        "theme": "Design", "default": "Standard", "dark": "Dunkel", "light": "Hell", "auto": "Automatisch (PC)",
        "actions": "Auszuführende Aktionen", "actions_hint": "Mit Kommas: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Verzögerung zwischen Aktionen (ms)", "hold": "Tastendruckdauer (ms)", "min": "Min.", "max": "Max.",
        "window": "BongoCat-Fenstertitel", "find_window": "Fenster auswählen",
        "window_help": "Wähle das Fenster, das BBC steuern soll. Standard: BongoCat.",
        "focus": "Stoppen, wenn BongoCat den Fokus verliert", "topmost": "BBC im Vordergrund halten", "save": "Speichern", "cancel": "Abbrechen",
        "saved": "Einstellungen gespeichert.", "invalid": "Gültige Werte eingeben.", "invalid_actions": "Mindestens eine Aktion hinzufügen.",
        "title": APP_NAME, "hint": "BBC sendet nur Aktionen, solange das ausgewählte BongoCat-Fenster aktiv ist.",
        "version": "Version 1.0.0", "creator": "Erstellt von Nuunez", "select_title": "BongoCat-Fenster auswählen",
        "select_hint": "Wähle das Fenster, das BBC steuern soll:", "refresh": "Aktualisieren", "use_selected": "Auswahl verwenden",
    },
    "zh": {
        "settings": "设置", "status_stopped": "● 已停止", "status_running": "● 运行中", "status_not_found": "未找到 BongoCat 窗口",
        "status_focus": "已停止：BongoCat 失去焦点", "status_error": "已停止：输入错误", "status_hotkey_error": "无法注册切换键",
        "start": "▶ 开始", "stop": "■ 停止", "toggle": "切换键", "language": "语言", "theme": "主题",
        "default": "默认", "dark": "深色", "light": "浅色", "auto": "自动（电脑）", "actions": "要执行的操作",
        "actions_hint": "使用逗号：a, s, d, LEFT_CLICK, RIGHT_CLICK", "interval": "操作间隔（毫秒）", "hold": "按键保持时间（毫秒）",
        "min": "最小", "max": "最大", "window": "BongoCat 窗口标题", "find_window": "选择窗口",
        "window_help": "选择 BBC 要控制的窗口。默认：BongoCat。", "focus": "BongoCat 失去焦点时停止", "topmost": "保持 BBC 置顶",
        "save": "保存", "cancel": "取消", "saved": "设置已保存。", "invalid": "请输入有效值。", "invalid_actions": "至少添加一个操作。",
        "title": APP_NAME, "hint": "BBC 只会在选中的 BongoCat 窗口处于活动状态时发送操作。", "version": "版本 1.0.0",
        "creator": "由 Nuunez 创建", "select_title": "选择 BongoCat 窗口", "select_hint": "选择 BBC 要控制的窗口：",
        "refresh": "刷新", "use_selected": "使用所选窗口",
    },
    "ja": {
        "settings": "設定", "status_stopped": "● 停止中", "status_running": "● 実行中", "status_not_found": "BongoCat のウィンドウが見つかりません",
        "status_focus": "停止：BongoCat が非アクティブになりました", "status_error": "停止：入力エラー", "status_hotkey_error": "切替キーを登録できませんでした",
        "start": "▶ 開始", "stop": "■ 停止", "toggle": "切替キー", "language": "言語", "theme": "テーマ",
        "default": "既定", "dark": "ダーク", "light": "ライト", "auto": "自動（PC）", "actions": "実行する操作",
        "actions_hint": "カンマ区切り：a, s, d, LEFT_CLICK, RIGHT_CLICK", "interval": "操作間隔（ms）", "hold": "キー保持時間（ms）",
        "min": "最小", "max": "最大", "window": "BongoCat ウィンドウタイトル", "find_window": "ウィンドウを選択",
        "window_help": "BBC が操作するウィンドウを選択します。既定：BongoCat。", "focus": "BongoCat が非アクティブになったら停止",
        "topmost": "BBC を常に手前に表示", "save": "保存", "cancel": "キャンセル", "saved": "設定を保存しました。",
        "invalid": "有効な値を入力してください。", "invalid_actions": "少なくとも1つの操作を追加してください。", "title": APP_NAME,
        "hint": "BBC は選択した BongoCat ウィンドウがアクティブな場合のみ操作を送信します。", "version": "バージョン 1.0.0",
        "creator": "Nuunez 作成", "select_title": "BongoCat ウィンドウを選択", "select_hint": "BBC が操作するウィンドウを選択：",
        "refresh": "更新", "use_selected": "選択を使用",
    },
    "ko": {
        "settings": "설정", "status_stopped": "● 중지됨", "status_running": "● 실행 중", "status_not_found": "BongoCat 창을 찾을 수 없습니다",
        "status_focus": "중지됨: BongoCat 포커스를 잃었습니다", "status_error": "중지됨: 입력 오류", "status_hotkey_error": "전환 키를 등록할 수 없습니다",
        "start": "▶ 시작", "stop": "■ 중지", "toggle": "전환 키", "language": "언어", "theme": "테마", "default": "기본",
        "dark": "어둡게", "light": "밝게", "auto": "자동(PC)", "actions": "실행할 동작", "actions_hint": "쉼표 사용: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "동작 간 지연 시간(ms)", "hold": "키 유지 시간(ms)", "min": "최소", "max": "최대", "window": "BongoCat 창 제목",
        "find_window": "창 선택", "window_help": "BBC가 제어할 창을 선택하세요. 기본값: BongoCat.", "focus": "BongoCat 포커스를 잃으면 중지",
        "topmost": "BBC를 항상 위에 표시", "save": "저장", "cancel": "취소", "saved": "설정이 저장되었습니다.", "invalid": "유효한 값을 입력하세요.",
        "invalid_actions": "하나 이상의 동작을 추가하세요.", "title": APP_NAME, "hint": "BBC는 선택한 BongoCat 창이 활성 상태일 때만 동작을 보냅니다.",
        "version": "버전 1.0.0", "creator": "Nuunez 제작", "select_title": "BongoCat 창 선택", "select_hint": "BBC가 제어할 창을 선택하세요:",
        "refresh": "새로 고침", "use_selected": "선택 사용",
    },
    "it": {
        "settings": "Impostazioni", "status_stopped": "● Arrestato", "status_running": "● In esecuzione", "status_not_found": "Finestra BongoCat non trovata",
        "status_focus": "Arrestato: BongoCat ha perso il focus", "status_error": "Arrestato: errore di input", "status_hotkey_error": "Impossibile registrare il tasto",
        "start": "▶ Avvia", "stop": "■ Ferma", "toggle": "Tasto di attivazione", "language": "Lingua", "theme": "Tema", "default": "Predefinito",
        "dark": "Scuro", "light": "Chiaro", "auto": "Automatico (PC)", "actions": "Azioni da eseguire", "actions_hint": "Usa virgole: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Intervallo tra azioni (ms)", "hold": "Durata pressione (ms)", "min": "Min.", "max": "Max.", "window": "Titolo finestra BongoCat",
        "find_window": "Seleziona finestra", "window_help": "Scegli la finestra che BBC deve controllare. Predefinita: BongoCat.", "focus": "Ferma se BongoCat perde il focus",
        "topmost": "Mantieni BBC in primo piano", "save": "Salva", "cancel": "Annulla", "saved": "Impostazioni salvate.", "invalid": "Inserisci valori validi.",
        "invalid_actions": "Aggiungi almeno un'azione.", "title": APP_NAME, "hint": "BBC invia azioni solo quando la finestra BongoCat selezionata è attiva.",
        "version": "Versione 1.0.0", "creator": "Creato da Nuunez", "select_title": "Seleziona finestra BongoCat", "select_hint": "Seleziona la finestra che BBC deve controllare:",
        "refresh": "Aggiorna", "use_selected": "Usa selezionata",
    },
    "nl": {
        "settings": "Instellingen", "status_stopped": "● Gestopt", "status_running": "● Actief", "status_not_found": "BongoCat-venster niet gevonden",
        "status_focus": "Gestopt: BongoCat verloor focus", "status_error": "Gestopt: invoerfout", "status_hotkey_error": "Activeringstoets kon niet worden geregistreerd",
        "start": "▶ Start", "stop": "■ Stop", "toggle": "Activeringstoets", "language": "Taal", "theme": "Thema", "default": "Standaard",
        "dark": "Donker", "light": "Licht", "auto": "Automatisch (pc)", "actions": "Uit te voeren acties", "actions_hint": "Gebruik komma's: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Vertraging tussen acties (ms)", "hold": "Toetsduur (ms)", "min": "Min.", "max": "Max.", "window": "Titel van BongoCat-venster",
        "find_window": "Venster selecteren", "window_help": "Kies het venster dat BBC moet bedienen. Standaard: BongoCat.", "focus": "Stop als BongoCat focus verliest",
        "topmost": "BBC altijd bovenaan", "save": "Opslaan", "cancel": "Annuleren", "saved": "Instellingen opgeslagen.", "invalid": "Voer geldige waarden in.",
        "invalid_actions": "Voeg minstens één actie toe.", "title": APP_NAME, "hint": "BBC verstuurt alleen acties terwijl het geselecteerde BongoCat-venster actief is.",
        "version": "Versie 1.0.0", "creator": "Gemaakt door Nuunez", "select_title": "BongoCat-venster selecteren", "select_hint": "Selecteer het venster dat BBC moet bedienen:",
        "refresh": "Vernieuwen", "use_selected": "Selectie gebruiken",
    },
    "pl": {
        "settings": "Ustawienia", "status_stopped": "● Zatrzymano", "status_running": "● Działa", "status_not_found": "Nie znaleziono okna BongoCat",
        "status_focus": "Zatrzymano: BongoCat stracił fokus", "status_error": "Zatrzymano: błąd wejścia", "status_hotkey_error": "Nie można zarejestrować klawisza",
        "start": "▶ Uruchom", "stop": "■ Zatrzymaj", "toggle": "Klawisz przełączania", "language": "Język", "theme": "Motyw", "default": "Domyślny",
        "dark": "Ciemny", "light": "Jasny", "auto": "Automatyczny (PC)", "actions": "Wykonywane akcje", "actions_hint": "Użyj przecinków: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Opóźnienie między akcjami (ms)", "hold": "Czas przytrzymania (ms)", "min": "Min.", "max": "Maks.", "window": "Tytuł okna BongoCat",
        "find_window": "Wybierz okno", "window_help": "Wybierz okno, którym ma sterować BBC. Domyślnie: BongoCat.", "focus": "Zatrzymaj, gdy BongoCat straci fokus",
        "topmost": "Zawsze pokazuj BBC na wierzchu", "save": "Zapisz", "cancel": "Anuluj", "saved": "Ustawienia zapisane.", "invalid": "Wprowadź poprawne wartości.",
        "invalid_actions": "Dodaj co najmniej jedną akcję.", "title": APP_NAME, "hint": "BBC wysyła akcje tylko, gdy wybrane okno BongoCat jest aktywne.",
        "version": "Wersja 1.0.0", "creator": "Utworzone przez Nuunez", "select_title": "Wybierz okno BongoCat", "select_hint": "Wybierz okno, którym ma sterować BBC:",
        "refresh": "Odśwież", "use_selected": "Użyj wybranego",
    },
    "ru": {
        "settings": "Настройки", "status_stopped": "● Остановлено", "status_running": "● Работает", "status_not_found": "Окно BongoCat не найдено",
        "status_focus": "Остановлено: BongoCat потерял фокус", "status_error": "Остановлено: ошибка ввода", "status_hotkey_error": "Не удалось зарегистрировать клавишу",
        "start": "▶ Запуск", "stop": "■ Стоп", "toggle": "Клавиша переключения", "language": "Язык", "theme": "Тема", "default": "По умолчанию",
        "dark": "Тёмная", "light": "Светлая", "auto": "Автоматически (ПК)", "actions": "Действия", "actions_hint": "Через запятую: a, s, d, LEFT_CLICK, RIGHT_CLICK",
        "interval": "Задержка между действиями (мс)", "hold": "Время удержания (мс)", "min": "Мин.", "max": "Макс.", "window": "Заголовок окна BongoCat",
        "find_window": "Выбрать окно", "window_help": "Выберите окно, которым должен управлять BBC. По умолчанию: BongoCat.", "focus": "Останавливать при потере фокуса BongoCat",
        "topmost": "Держать BBC поверх окон", "save": "Сохранить", "cancel": "Отмена", "saved": "Настройки сохранены.", "invalid": "Введите корректные значения.",
        "invalid_actions": "Добавьте хотя бы одно действие.", "title": APP_NAME, "hint": "BBC отправляет действия только когда выбранное окно BongoCat активно.",
        "version": "Версия 1.0.0", "creator": "Создано Nuunez", "select_title": "Выбор окна BongoCat", "select_hint": "Выберите окно, которым должен управлять BBC:",
        "refresh": "Обновить", "use_selected": "Использовать выбранное",
    },
}


def detect_pc_language():
    try:
        buf = ctypes.create_unicode_buffer(85)
        if ctypes.windll.kernel32.GetUserDefaultLocaleName(buf, 85):
            locale = buf.value.lower()
            code = locale.split("-")[0]
            supported = {"en", "pt", "es", "fr", "de", "zh", "ja", "ko", "it", "nl", "pl", "ru"}
            return code if code in supported else "en"
    except Exception:
        pass
    return "en"


def detect_windows_theme():
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        key.Close()
        return "light" if value else "dark"
    except Exception:
        return "dark"


def load_config():
    config = dict(DEFAULT_CONFIG)
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("r", encoding="utf-8") as file:
                saved = json.load(file)
            if isinstance(saved, dict):
                config.update(saved)
    except Exception:
        pass
    return config


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)


config = load_config()
running = False
lock = threading.Lock()
stop_event = threading.Event()
root = None
status_label = None
start_button = None
hotkey_handle = None


def tr(key):
    language = config.get("language", "auto")
    if language == "auto":
        language = detect_pc_language()
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)


def resolved_theme():
    theme = config.get("theme", "default")
    return detect_windows_theme() if theme == "default" else theme


def get_colors():
    if resolved_theme() == "light":
        return {
            "bg": "#f3f3f3",
            "panel": "#ffffff",
            "fg": "#202020",
            "muted": "#666666",
            "button": "#e5e5e5",
            "button_active": "#d5d5d5",
            "green": "#078a42",
            "red": "#c62828",
            "orange": "#aa6b00",
            "border": "#cccccc",
        }
    return {
        "bg": "#1e1e2e",
        "panel": "#242436",
        "fg": "#cdd6f4",
        "muted": "#8a8aa0",
        "button": "#313244",
        "button_active": "#45475a",
        "green": "#00d982",
        "red": "#ff5555",
        "orange": "#ffb86c",
        "border": "#45475a",
    }


def enum_visible_windows():
    windows = []

    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd).strip()
        if not title:
            return
        try:
            if win32gui.IsIconic(hwnd):
                return
        except Exception:
            pass
        windows.append((title, hwnd))

    win32gui.EnumWindows(callback, None)
    windows.sort(key=lambda item: item[0].lower())
    return windows


def find_bongocat():
    title = str(config.get("window_title", "BongoCat")).strip()
    if not title:
        return None
    hwnd = win32gui.FindWindow(None, title)
    return hwnd if hwnd and win32gui.IsWindow(hwnd) else None


def focus_bongocat():
    hwnd = find_bongocat()
    if not hwnd:
        return None
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return hwnd
    except Exception:
        return None


def is_bongocat_foreground():
    hwnd = find_bongocat()
    if not hwnd:
        return False
    try:
        return win32gui.GetForegroundWindow() == hwnd
    except Exception:
        return False


def parse_actions():
    raw = config.get("actions", [])
    if isinstance(raw, str):
        raw = raw.split(",")
    return [str(item).strip() for item in raw if str(item).strip()]


def random_hold_seconds():
    low = max(0, int(config.get("hold_min_ms", 30)))
    high = max(low, int(config.get("hold_max_ms", 40)))
    return random.uniform(low, high) / 1000.0


def random_interval_seconds():
    low = max(0, int(config.get("interval_min_ms", 20)))
    high = max(low, int(config.get("interval_max_ms", 30)))
    return random.uniform(low, high) / 1000.0


def do_action(action):
    action_upper = action.upper()

    if action_upper in {"LEFT_CLICK", "LCLICK", "CLICK"}:
        pydirectinput.mouseDown(button="left")
        time.sleep(random_hold_seconds())
        pydirectinput.mouseUp(button="left")
        return

    if action_upper in {"RIGHT_CLICK", "RCLICK"}:
        pydirectinput.mouseDown(button="right")
        time.sleep(random_hold_seconds())
        pydirectinput.mouseUp(button="right")
        return

    pydirectinput.keyDown(action)
    time.sleep(random_hold_seconds())
    pydirectinput.keyUp(action)


def set_status(text, color=None):
    if status_label is None or root is None:
        return
    colors = get_colors()
    color = color or colors["fg"]
    root.after(0, lambda: status_label.config(text=text, fg=color))


def update_main_button():
    if start_button is None or root is None:
        return
    with lock:
        active = running
    label = tr("stop" if active else "start")
    key = str(config.get("toggle_key", "f8")).upper()
    root.after(0, lambda: start_button.config(text=f"{label}  [{key}]"))


def set_running(state, reason=None):
    global running

    if state:
        hwnd = focus_bongocat()
        if not hwnd:
            with lock:
                running = False
            set_status(tr("status_not_found"), get_colors()["orange"])
            update_main_button()
            return False
        with lock:
            running = True
        set_status(tr("status_running"), get_colors()["green"])
    else:
        with lock:
            running = False
        if reason == "focus":
            set_status(tr("status_focus"), get_colors()["orange"])
        elif reason == "error":
            set_status(tr("status_error"), get_colors()["red"])
        else:
            set_status(tr("status_stopped"), get_colors()["red"])

    update_main_button()
    return True


def toggle_running():
    with lock:
        current = running
    set_running(not current)


def register_hotkey():
    global hotkey_handle

    if hotkey_handle is not None:
        try:
            keyboard.remove_hotkey(hotkey_handle)
        except Exception:
            pass
        hotkey_handle = None

    key = str(config.get("toggle_key", "f8")).strip().lower()
    if not key:
        return False

    try:
        hotkey_handle = keyboard.add_hotkey(key, toggle_running, suppress=False)
        return True
    except Exception as exc:
        print(f"[hotkey] {exc}")
        set_status(tr("status_hotkey_error"), get_colors()["orange"])
        return False


def select_window_dialog(parent):
    colors = get_colors()
    dialog = tk.Toplevel(parent)
    dialog.title(tr("select_title"))
    dialog.geometry("520x430")
    dialog.resizable(False, False)
    dialog.configure(bg=colors["bg"])
    dialog.transient(parent)
    dialog.grab_set()

    tk.Label(
        dialog,
        text=tr("select_hint"),
        bg=colors["bg"],
        fg=colors["fg"],
        font=("Segoe UI", 10),
    ).pack(anchor="w", padx=18, pady=(16, 8))

    frame = tk.Frame(dialog, bg=colors["bg"])
    frame.pack(fill="both", expand=True, padx=18)

    scrollbar = ttk.Scrollbar(frame, orient="vertical")
    listbox = tk.Listbox(
        frame,
        bg=colors["panel"],
        fg=colors["fg"],
        selectbackground=colors["border"],
        relief="flat",
        activestyle="none",
        yscrollcommand=scrollbar.set,
    )
    scrollbar.configure(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    window_pairs = []

    def refresh():
        nonlocal window_pairs
        window_pairs = enum_visible_windows()
        listbox.delete(0, tk.END)
        current_title = str(config.get("window_title", "BongoCat"))
        for title, _hwnd in window_pairs:
            prefix = "✓ " if title == current_title else "  "
            listbox.insert(tk.END, prefix + title)
        for index, (title, _hwnd) in enumerate(window_pairs):
            if title == current_title:
                listbox.selection_set(index)
                listbox.see(index)
                break

    refresh()

    buttons = tk.Frame(dialog, bg=colors["bg"])
    buttons.pack(fill="x", padx=18, pady=14)

    def use_selected():
        selection = listbox.curselection()
        if not selection:
            return
        title, _hwnd = window_pairs[selection[0]]
        config["window_title"] = title
        dialog.destroy()

    tk.Button(
        buttons,
        text=tr("refresh"),
        command=refresh,
        bg=colors["button"],
        fg=colors["fg"],
        relief="flat",
        padx=12,
        pady=7,
    ).pack(side="left")
    tk.Button(
        buttons,
        text=tr("use_selected"),
        command=use_selected,
        bg=colors["button"],
        fg=colors["fg"],
        relief="flat",
        padx=12,
        pady=7,
    ).pack(side="right")


def build_settings():
    colors = get_colors()
    win = tk.Toplevel(root)
    win.title(f"{APP_NAME} — {tr('settings')}")
    win.geometry("620x620")
    win.resizable(False, False)
    win.configure(bg=colors["bg"])
    win.transient(root)
    win.grab_set()

    vars_ = {
        "language": tk.StringVar(value=config.get("language", "auto")),
        "theme": tk.StringVar(value=config.get("theme", "default")),
        "toggle": tk.StringVar(value=config.get("toggle_key", "f8")),
        "window": tk.StringVar(value=config.get("window_title", "BongoCat")),
        "actions": tk.StringVar(value=", ".join(config.get("actions", []))),
        "imin": tk.StringVar(value=str(config.get("interval_min_ms", 20))),
        "imax": tk.StringVar(value=str(config.get("interval_max_ms", 30))),
        "hmin": tk.StringVar(value=str(config.get("hold_min_ms", 30))),
        "hmax": tk.StringVar(value=str(config.get("hold_max_ms", 40))),
        "focus": tk.BooleanVar(value=config.get("stop_when_focus_lost", True)),
        "topmost": tk.BooleanVar(value=config.get("always_on_top", True)),
    }

    frame = tk.Frame(win, bg=colors["bg"])
    frame.pack(fill="both", expand=True, padx=22, pady=18)
    frame.columnconfigure(1, weight=1)

    def label(text, row):
        tk.Label(
            frame,
            text=text,
            bg=colors["bg"],
            fg=colors["fg"],
            anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=7, padx=(0, 14))

    label(tr("language"), 0)
    ttk.Combobox(
        frame,
        textvariable=vars_["language"],
        state="readonly",
        values=[
            "auto", "en", "pt", "es", "fr", "de", "zh", "ja", "ko",
            "it", "nl", "pl", "ru"
        ],
        width=28,
    ).grid(row=0, column=1, sticky="ew", pady=7)

    label(tr("theme"), 1)
    ttk.Combobox(
        frame,
        textvariable=vars_["theme"],
        state="readonly",
        values=["default", "dark", "light"],
        width=28,
    ).grid(row=1, column=1, sticky="ew", pady=7)

    label(tr("toggle"), 2)
    tk.Entry(
        frame,
        textvariable=vars_["toggle"],
        bg=colors["panel"],
        fg=colors["fg"],
        insertbackground=colors["fg"],
        relief="flat",
    ).grid(row=2, column=1, sticky="ew", pady=7)

    label(tr("window"), 3)
    window_frame = tk.Frame(frame, bg=colors["bg"])
    window_frame.grid(row=3, column=1, sticky="ew", pady=7)
    window_frame.columnconfigure(0, weight=1)
    tk.Entry(
        window_frame,
        textvariable=vars_["window"],
        bg=colors["panel"],
        fg=colors["fg"],
        insertbackground=colors["fg"],
        relief="flat",
    ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

    def open_selector():
        select_window_dialog(win)
        vars_["window"].set(config.get("window_title", "BongoCat"))

    tk.Button(
        window_frame,
        text=tr("find_window"),
        command=open_selector,
        bg=colors["button"],
        fg=colors["fg"],
        activebackground=colors["button_active"],
        activeforeground=colors["fg"],
        relief="flat",
        padx=10,
        pady=5,
    ).grid(row=0, column=1)

    tk.Label(
        frame,
        text=tr("window_help"),
        bg=colors["bg"],
        fg=colors["muted"],
    ).grid(row=4, column=1, sticky="w", pady=(0, 5))

    label(tr("actions"), 5)
    tk.Entry(
        frame,
        textvariable=vars_["actions"],
        bg=colors["panel"],
        fg=colors["fg"],
        insertbackground=colors["fg"],
        relief="flat",
    ).grid(row=5, column=1, sticky="ew", pady=7)
    tk.Label(
        frame,
        text=tr("actions_hint"),
        bg=colors["bg"],
        fg=colors["muted"],
    ).grid(row=6, column=1, sticky="w")

    label(tr("interval"), 7)
    interval_frame = tk.Frame(frame, bg=colors["bg"])
    interval_frame.grid(row=7, column=1, sticky="w", pady=7)
    tk.Entry(interval_frame, textvariable=vars_["imin"], width=9).pack(side="left")
    tk.Label(interval_frame, text=f"  {tr('min')}    ", bg=colors["bg"], fg=colors["muted"]).pack(side="left")
    tk.Entry(interval_frame, textvariable=vars_["imax"], width=9).pack(side="left")
    tk.Label(interval_frame, text=f"  {tr('max')}", bg=colors["bg"], fg=colors["muted"]).pack(side="left")

    label(tr("hold"), 8)
    hold_frame = tk.Frame(frame, bg=colors["bg"])
    hold_frame.grid(row=8, column=1, sticky="w", pady=7)
    tk.Entry(hold_frame, textvariable=vars_["hmin"], width=9).pack(side="left")
    tk.Label(hold_frame, text=f"  {tr('min')}    ", bg=colors["bg"], fg=colors["muted"]).pack(side="left")
    tk.Entry(hold_frame, textvariable=vars_["hmax"], width=9).pack(side="left")
    tk.Label(hold_frame, text=f"  {tr('max')}", bg=colors["bg"], fg=colors["muted"]).pack(side="left")

    tk.Checkbutton(
        frame,
        text=tr("focus"),
        variable=vars_["focus"],
        bg=colors["bg"],
        fg=colors["fg"],
        selectcolor=colors["panel"],
        activebackground=colors["bg"],
        activeforeground=colors["fg"],
    ).grid(row=9, column=0, columnspan=2, sticky="w", pady=8)

    tk.Checkbutton(
        frame,
        text=tr("topmost"),
        variable=vars_["topmost"],
        bg=colors["bg"],
        fg=colors["fg"],
        selectcolor=colors["panel"],
        activebackground=colors["bg"],
        activeforeground=colors["fg"],
    ).grid(row=10, column=0, columnspan=2, sticky="w")

    buttons = tk.Frame(frame, bg=colors["bg"])
    buttons.grid(row=11, column=0, columnspan=2, pady=24, sticky="e")

    def save():
        try:
            interval_min = int(vars_["imin"].get())
            interval_max = int(vars_["imax"].get())
            hold_min = int(vars_["hmin"].get())
            hold_max = int(vars_["hmax"].get())
            if min(interval_min, interval_max, hold_min, hold_max) < 0:
                raise ValueError
            if interval_min > interval_max or hold_min > hold_max:
                raise ValueError

            actions = [item.strip() for item in vars_["actions"].get().split(",") if item.strip()]
            if not actions:
                messagebox.showerror(APP_NAME, tr("invalid_actions"), parent=win)
                return

            toggle_key = vars_["toggle"].get().strip().lower()
            window_title = vars_["window"].get().strip()
            if not toggle_key or not window_title:
                raise ValueError

            config.update(
                {
                    "language": vars_["language"].get(),
                    "theme": vars_["theme"].get(),
                    "toggle_key": toggle_key,
                    "window_title": window_title,
                    "actions": actions,
                    "interval_min_ms": interval_min,
                    "interval_max_ms": interval_max,
                    "hold_min_ms": hold_min,
                    "hold_max_ms": hold_max,
                    "stop_when_focus_lost": bool(vars_["focus"].get()),
                    "always_on_top": bool(vars_["topmost"].get()),
                }
            )
            save_config(config)
            register_hotkey()
            root.attributes("-topmost", config["always_on_top"])
            win.destroy()
            rebuild_main()
        except ValueError:
            messagebox.showerror(APP_NAME, tr("invalid"), parent=win)

    tk.Button(
        buttons,
        text=tr("cancel"),
        command=win.destroy,
        bg=colors["button"],
        fg=colors["fg"],
        relief="flat",
        padx=15,
        pady=7,
    ).pack(side="right", padx=5)
    tk.Button(
        buttons,
        text=tr("save"),
        command=save,
        bg=colors["button"],
        fg=colors["fg"],
        relief="flat",
        padx=15,
        pady=7,
    ).pack(side="right")


def rebuild_main():
    global status_label, start_button
    colors = get_colors()
    root.configure(bg=colors["bg"])

    for child in root.winfo_children():
        child.destroy()

    title_font = ("Segoe UI", 15, "bold")
    status_font = ("Segoe UI", 11)
    button_font = ("Segoe UI", 10, "bold")

    tk.Label(
        root,
        text=APP_NAME,
        font=title_font,
        bg=colors["bg"],
        fg=colors["fg"],
    ).pack(pady=(18, 3))

    tk.Label(
        root,
        text=tr("version"),
        font=("Segoe UI", 8),
        bg=colors["bg"],
        fg=colors["muted"],
    ).pack()

    status_label = tk.Label(
        root,
        text=tr("status_running" if running else "status_stopped"),
        font=status_font,
        bg=colors["bg"],
        fg=colors["green"] if running else colors["red"],
    )
    status_label.pack(pady=(10, 2))

    start_button = tk.Button(
        root,
        text=f"{tr('stop' if running else 'start')}  [{str(config.get('toggle_key', 'f8')).upper()}]",
        font=button_font,
        bg=colors["button"],
        fg=colors["fg"],
        activebackground=colors["button_active"],
        activeforeground=colors["fg"],
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=toggle_running,
    )
    start_button.pack(pady=10)

    tk.Button(
        root,
        text=f"⚙ {tr('settings')}",
        bg=colors["button"],
        fg=colors["fg"],
        activebackground=colors["button_active"],
        activeforeground=colors["fg"],
        relief="flat",
        padx=12,
        pady=6,
        command=build_settings,
    ).pack(pady=2)

    tk.Label(
        root,
        text=tr("hint"),
        font=("Segoe UI", 8),
        bg=colors["bg"],
        fg=colors["muted"],
        wraplength=420,
    ).pack(pady=(12, 2))

    tk.Label(
        root,
        text=tr("creator"),
        font=("Segoe UI", 8),
        bg=colors["bg"],
        fg=colors["muted"],
    ).pack(pady=(2, 8))

    root.title("BBC")
    root.attributes("-topmost", bool(config.get("always_on_top", True)))


def resource_path(*parts):
    # Works both from source and from a PyInstaller one-file executable.
    base = Path(getattr(__import__("sys"), "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base.joinpath(*parts)


def set_app_icon():
    icon_path = resource_path("assets", "BBC.ico")
    if icon_path.exists():
        try:
            root.iconbitmap(str(icon_path))
        except Exception:
            pass


def on_close():
    global running
    with lock:
        running = False
    stop_event.set()

    try:
        keyboard.unhook_all_hotkeys()
    except Exception:
        pass

    root.destroy()


def main():
    global root

    pydirectinput.PAUSE = 0
    pydirectinput.FAILSAFE = True

    root = tk.Tk()
    root.geometry("450x310")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_close)
    set_app_icon()
    rebuild_main()

    register_hotkey()
    threading.Thread(target=worker, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()
