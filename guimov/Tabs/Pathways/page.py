from .elements import *

layout = html.Div(
    className='guimov_layout_pa',
    children=[
        html.Div(
            className="guimov_left_pa",
            children=[
                GeneDiffs_title,
                mod_dropdown_pa,
                tooltip_mod_dropdown_pa,
                gene_name_pa,
                tooltip_gene_name_pa,
                texte_area_pa,
                tooltip_texte_area_pa,
                pathway_name_pa,
                tooltip_pathway_name_pa,
                input_file_pa,
                tooltip_input_file_pa,
                button_run_pa,
                tooltip_button_run_pa,
                label_error_pa,
                update_from_pa,
            ],
        ),
        html.Div(
            className='guimov_right_pa',
            children=[
                table_pa,
                loading_pa,
                alert_pa,
            ],
        ),
    ]
)
