from applications_utils.streamlit_utils import display_loader
from datetime import datetime
import json
from loguru import logger
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import JsCode
import streamlit as st
import streamlit.components.v1 as components
from streamlit_tags import st_tags


DEFAULT_EVENTS = ['LOGIN', 'RESET_PASSWORD_TOKEN_SENT_SUCCESS', 'MAJ_INTERVENANT',
'MISE_A_DISPOSITION', 'LOGOUT', 'CHANGE_DEVICE',
'AJOUTER_BENEFICIAIRE', 'EFFECTUER_VIREMENT']

def highlight_price():
    code = """
        function(params) {
            let value = params.value.replace('MAD', '').trim();
            if (value === "" || isNaN(value)) {
                console.log('Invalid or empty value:', params.value);
                return "";
            }
            
            let sign = value[0];  // '+' or '-'
            let number = parseFloat(value);
            let absNumber = Math.abs(number);

            // Set the default RGB color based on the sign
            let backgroundColor = sign === '+' ? 'rgba(68, 206, 27, {opacity})' : 'rgba(229, 31, 31, {opacity})';  // Green for +, Red for -
            let maxNumber = 100000;
            let minOpacity = 0.1;
            let maxOpacity = 1;
            let opacity = Math.min(maxOpacity, minOpacity + (absNumber / maxNumber) * (maxOpacity - minOpacity));
            let color = opacity > 0.3 ? 'white' : 'gray';

            // Injecting calculated opacity into the backgroundColor
            backgroundColor = backgroundColor.replace('{opacity}', opacity);

            return { color:color , backgroundColor: backgroundColor };
        }
    """
    return JsCode(code)

def highlight_scores():
    code = """
        function(params) {
            let value = params.value.replace('%', '').trim();
            if (isNaN(value)) {
                console.log('Non-numeric value encountered:', params.value);
                return "";
            }
            let score = parseInt(value);
            let opacity = 0.3 + (score / 100) * 0.7;  // Calculating opacity
            let color = opacity > 0.3 ? 'white' : 'gray';

            // Applying RGB colors with dynamic opacity
            if (score < 20) {
                return { color: color, backgroundColor: 'rgba(80, 184, 50, ' + opacity + ')' };  // Green
            } else if (score < 40) {
                return { color: color, backgroundColor: 'rgba(187, 219, 68, ' + opacity + ')' };  // Light Green
            } else if (score < 60) {
                return { color: color, backgroundColor: 'rgba(247, 227, 121, ' + opacity + ')' };  // Yellow
            } else if (score < 80) {
                return { color: color, backgroundColor: 'rgba(242, 161, 52, ' + opacity + ')' };  // Orange
            } else if (score <= 100) {
                return { color: color, backgroundColor: 'rgba(219, 61, 61, ' + opacity + ')' };  // Red
            } else {
                return "";
            }
        };
    """
    return JsCode(code)


def animate_loader(message):
    def decorate(action):
        def load_wrapper(*args, **kwargs):
            loader = st.markdown(display_loader(message), unsafe_allow_html=True)
            with loader:
                result = action(*args, **kwargs) 
            loader.empty()
            return result
        return load_wrapper
    return decorate

def display_fraude_data(data):
    if settings := st.session_state.get("settings"):
        score_reset = settings["score_reset"]
        score_device = settings["score_device"]
        display_types = settings["display_types"]
    else:
        score_reset = 65
        score_device = 90
        display_types = ["Device", "Reset"]
    if not data.empty:
        logger.info("Displaying fraud data with settings :")
        logger.info(f"Score Reset : {score_reset}")
        logger.info(f"Score Device : {score_device}")
        logger.info(f"Display Types : {display_types}")
        filter_condition = (data.index < 0)
        
        if "Reset" in display_types:
            filter_condition_reset = (data["Score Reset"].str.strip().str[:-1].astype(float) >= score_reset)
            filter_condition = filter_condition | filter_condition_reset
        
        if "Device" in display_types:
            filter_condition_device = (data["Score Device"].str.strip().str[:-1].astype(float) >= score_device)
            filter_condition = filter_condition | filter_condition_device

        # Apply the combined filter condition to the dataframe
        data = data[filter_condition]
        data = data.sort_values(by=["Identifiant Client","Date"])

    st.write("")
    st.write("")
    st.write("#### Liste des alertes")
    st.write("")

    builder = GridOptionsBuilder.from_dataframe(data)
    builder.configure_selection(selection_mode="multiple", use_checkbox=False)
    builder.configure_pagination(
        enabled=True, paginationAutoPageSize=False, paginationPageSize=12
    )
    builder.configure_auto_height(autoHeight=False)
    builder.configure_default_column(
        groupable=True,
    )
    builder.configure_grid_options(
        enableRangeSelection=True,
        enableCharts=True,
        suppressExcelExport=True,
    )
    for col in data.columns:
        if col == "Identifiant":
            builder.configure_column(
                field=col,
                hide=True,
                supressToolPanel=True,
            )
        if col.startswith("Score"):
            builder.configure_column(
            field=col,
            cellStyle=highlight_scores(),
            )
        elif col == "Amount":
            builder.configure_column(
            field=col,
            cellStyle=highlight_price(),
            )
        else:
            builder.configure_column(
                field=col,
            )
    grid_options = builder.build()
    table =  AgGrid(
            data,
            gridOptions=grid_options,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
            theme="material",
            key="fraud_table_"+st.session_state["selected_date"]+"_"+str(score_reset)+"_"+str(score_device)+"_"+str("_".join(display_types)),
            enable_enterprise_modules = False,
        )
    tables = [k for k in st.session_state.keys() if k.startswith("fraud_table_") and k!="fraud_table_"+st.session_state["selected_date"]+"_"+str(score_reset)+"_"+str(score_device)+"_"+str("_".join(display_types))]
    for tbl in tables:
        del st.session_state[tbl]
        st.rerun()

    return table

def display_search_bar() -> str:
    selected_date = st.sidebar.date_input(
        "▸ Sélectionner une période",
        max_value=pd.to_datetime("2025-01-01"),
        key="input_date",
        value=datetime.now() - pd.Timedelta(days=1),
        label_visibility="visible",
    )
    return selected_date.strftime("%Y-%m-%d %H:%M:%S")

def display_advance_settings():
    st.sidebar.divider()
    with st.sidebar.popover("▸ Paramètres avancés"):
        default_colors = ("#D0D0D0", "#FFF")
        default_warm_event_color = ("#ff6347", "#FFF")
        # Score thresholds
        if settings := st.session_state.get("settings"):
            score_reset = settings["score_reset"]
            score_device = settings["score_device"]
            display_types = settings["display_types"]
            color_dict = settings["color_dict"]
        else:
            score_reset = 65
            score_device = 90
            display_types = ["Device", "Reset"]
            color_dict = {
                k: default_warm_event_color if k in ["RESET_PASSWORD_TOKEN_SENT_SUCCESS", "CHANGE_DEVICE"] else default_colors
                for k in DEFAULT_EVENTS
            }

        st.write("**Paramètres avancés**")
        st.divider()
        with st.expander("🤖 Paramètres modèles",expanded=True):
            st.text("Seuils de score")
            score_device = st.slider("Device", 0, 100, score_device, 5)
            score_reset = st.slider("Reset", 0, 100, score_reset, 5)
            types = st_tags(
                label='',
                text='Type de fraude',
                value=display_types,
                suggestions=['Device', 'Reset'],
                maxtags = 2,
                key='1')

        with st.expander("📡 Paramètres timeline"):


            tagged_events = st_tags(
                label='',
                text='Ajouter un événement',
                value=[event for event in color_dict.keys()],
                suggestions=DEFAULT_EVENTS,
                maxtags = len(DEFAULT_EVENTS),
                key='2')
            
            new_events = [event for event in tagged_events if event not in color_dict] # tagged but not in color_dict
            deleted_events = [event for event in color_dict if event not in tagged_events] # in color_dict but not tagged

            for event in new_events:
                color_dict[event] = default_colors
            
            for event in deleted_events:
                del color_dict[event]

            for event, (bg_color, text_color) in color_dict.items():
                st.text(event)
                bg_color = st.color_picker("Couleur de fond", bg_color, key=f"{event}_bg")
                text_color = st.color_picker("Couleur de texte", text_color, key=f"{event}_text")
                color_dict[event] = (bg_color, text_color)
        settings = {
            "score_reset": score_reset,
            "score_device": score_device,
            "display_types": types,
            "color_dict": color_dict
        }
        if settings != st.session_state.get("settings"):
            st.session_state["settings"] = settings


def display_timeline(data_df, selected_fraud_id):

    filtered_events = None
    if settings:= st.session_state.get("settings"):
        color_dict = settings["color_dict"]
        filtered_events = color_dict.keys()
    
    if filtered_events:
        data_df = data_df[data_df["Type"].isin(filtered_events)]

    target = "0"
    data_json = {"events": []}
    # order data_df by date
    data_df = data_df.sort_values(by="Date",ascending=False)
    data_df = data_df.reset_index()
    start_timer = False
    max_events = 100
    for index, row in data_df.iterrows():
        event, is_fraud = update_json(row, str(selected_fraud_id))
        if is_fraud:
            target = str(index)
            start_timer = True
        if start_timer:
            max_events -= 1
        if max_events == 0:
            break
        data_json["events"].append(event)

    timeline(data_json, height=600, target=target,color_dict=st.session_state["settings"]["color_dict"])


def update_json(selected_row: dict, selected_fraud_id: str) -> any:
    str_row_date = selected_row["Date"]
    id_index = selected_row["Identifiant"]
    description = selected_row["Message"]

    is_fraud = False
    if str(id_index).strip() == str(selected_fraud_id).strip():
        is_fraud = True
    description_dict = string_to_dict(description)
    title = (
        selected_row["Type"]
        .replace("_", " ")
        .capitalize()
        .replace("Attijari securite", "")
    )
    if description_dict.keys() == [] or description_dict.keys() == [""]:
        message = description
    else:
        message = "\n".join(
            ["<ul style='margin:0;padding:0;'>"]
            + [
                f"<li style='margin:0;padding:0;'>{key.capitalize()}: {value}</li>"
                for key, value in description_dict.items() if key
            ]
            + ["</ul>"]
        )
    card = ["<div style='height:150px;overflow-y:scroll;'>"]
    card += [
        f"{col_name.replace('_',' ').capitalize()} : {selected_row[col_name]}"
        if col_name != "Message"
        else f"{col_name.replace('_',' ').capitalize()}:{message}"
        for col_name in selected_row.index.to_list()[:-2]
    ]
    card += ["</div>"]
    card = "<br>".join(card)
    row_date = datetime.strptime(str_row_date, "%Y-%m-%d %H:%M:%S")
    datetime_dict  = {
        "year": row_date.year,
        "month": row_date.month,
        "day": row_date.day,
        "hour": row_date.hour,
        "minute": row_date.minute,
        "second": row_date.second,
    } 

    logger.info(datetime_dict)

    event = {
        "start_date": datetime_dict,
        "end_date": datetime_dict ,
        "text": {"headline": title, "text": card},
    }

    return event, is_fraud


def string_to_dict(input_string):
    parts = input_string.split()

    result_dict = {}

    current_key = None
    current_value = None

    for part in parts:
        if not part.startswith("["):
            current_key = part
        else:
            current_value = part.strip("[]")
            result_dict[current_key] = current_value

    return result_dict


def timeline(data, height=800, options=None, target=0,color_dict=None):
    """
    Create a new timeline component with configurable options.

    Parameters
    ----------
    data: str or dict
        String or dict in the timeline json format: https://timeline.knightlab.com/docs/json-format.html
    height: int or None
        Height of the timeline in px
    options: dict or None
        Dictionary of options to configure the timeline, as per https://timeline.knightlab.com/docs/options.html

    Returns
    -------
    static_component: Boolean
        Returns a static component with a timeline
    """

    # DEFAULT_OPTIONS no longer needs to be a string literal, but kept for reference
    DEFAULT_OPTIONS = {"initial_zoom": 2, "start_at_slide": target}
    DEFAULT_EVENTS_COLORS = {
        "RESET_PASSWORD_TOKEN_SENT_SUCCESS": ("#ff6347", "#FFF"),  # Cold red background, White text
        "CHANGE_DEVICE": ("#ff6347", "#FFF")  # Cold red background, White text
    }

    if options is None:
        options = DEFAULT_OPTIONS
    else:
        # Update DEFAULT_OPTIONS with any options provided by the user
        DEFAULT_OPTIONS.update(options)
        options = DEFAULT_OPTIONS

    # Options are now a dictionary; convert to a string when inserting into JavaScript
    options_text = json.dumps(options)

    # if string then to json
    if isinstance(data, str):
        data = json.loads(data)

    # json to string for data
    json_text = json.dumps(data)

    # load json
    source_param = "timeline_json"
    source_block = f"var {source_param} = {json_text};"
    # load css + js
    cdn_path = "https://cdn.knightlab.com/libs/timeline3/latest"
    css_block = f'<link title="timeline-styles" rel="stylesheet" href="{cdn_path}/css/timeline.css">'
    js_block = f'<script src="{cdn_path}/js/timeline.js"></script>'
    # Update the dictionary with the specified cold red color for specific events
    events_colors = DEFAULT_EVENTS_COLORS if color_dict is None else color_dict
    change_timemarker_background = """<script>
    function changeBackground() {
        var elements = document.getElementsByClassName("tl-timemarker-content-container");
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var event_type = element.innerText;
            """ + generate_switch_statement(events_colors) + """
        }
    }
    setTimeout(changeBackground, 1000);
    </script>"""
    

    # write html block
    htmlcode = (
        css_block
        + """ 
    """
        + js_block
        + """

        <div id='timeline-embed' style="width: 95%; height: """
        + str(height)
        + """px; margin: 1px;"></div>
    
        """
        + change_timemarker_background
        + """
        <script type="text/javascript">
            var additionalOptions = """
        + options_text
        + """;
            """
        + source_block
        + """
            timeline = new TL.Timeline('timeline-embed', """
        + source_param
        + """, additionalOptions);
        </script>"""
    )
    # return rendered html
    static_component = components.html(
        htmlcode,
        height=height,
    )

    return static_component


def generate_switch_statement(events_colors):
    switch_statement = '''switch (event_type.toLowerCase()) {\n'''  # Ensure code runs after DOM is fully loaded
    for event, (bg_color, text_color) in events_colors.items():
        event_formatted = event.replace("_", " ").lower()
        case_statement = f'''    case "{event_formatted}":
        element.style.backgroundColor = "{bg_color}";
        var h2Element = element.querySelector(".tl-timemarker-content .tl-timemarker-text h2.tl-headline");
        if (h2Element) {{
            h2Element.style.color = "{text_color}";
        }} else {{
            console.log("h2 element not found for event:", "{event_formatted}");
        }}
        break;
'''
        switch_statement += case_statement
    # Close the switch statement
    switch_statement += "}"

    return switch_statement


def scroll_listener():

    # Get the height of the container data-testid="stAppViewContainer"
    get_height_js = """
    function getContainerHeight() {
        var container = document.querySelector("section.main");
        return container.scrollHeight;
    }
    """

    # Get prev height from local storage
    local_storage_js = """
    function getLocalStorage(key) {
        return localStorage.getItem(key);
    }
    """

    # Scroll down the container if the height has changed
    scroll_down_js = """
    function scrollDown() {
        var prevHeight = getLocalStorage("prevHeight");
        if (prevHeight === null) {
            prevHeight = getContainerHeight();
            localStorage.setItem("prevHeight", prevHeight);
        }
        var currentHeight = getContainerHeight();
        if (currentHeight !== prevHeight) {
        console.log("Current height:", currentHeight);
        console.log("Previous height:", prevHeight);
            var container = document.querySelector("section.main");
            container.scrollTop = container.scrollHeight;
            localStorage.setItem("prevHeight", currentHeight);
        }
    }
    setInterval(scrollDown, 100);
    """
    code = "<script>"+get_height_js + local_storage_js + scroll_down_js+"</script>"
    logger.info(
        "Parsed code: \n%s"
        % code
    )

    return st.markdown(code, unsafe_allow_html=True)