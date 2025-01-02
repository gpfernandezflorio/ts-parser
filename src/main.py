import sys
from bibpy.base import Boom
from bibpy.archivos import contenidoDe_, existeArchivo_Acá
from parser import tokenizar, parsear, mostrarAST, mostrarTokens, mostrarDiff, eq_string

archivosTest = [
  "any_aliases",
  "block",
  "block_animations",
  "block_dragger",
  "block_svg",
  "blockly",
  "blockly_options",
  "blocks",
  "browser_events",
  "bubble_dragger",
  "bubbles/bubble",
  "bubbles/mini_workspace_bubble",
  "bubbles/text_bubble",
  "bubbles/textinput_bubble",
  "bubbles",
  "bump_objects",
  "clipboard/block_paster",
  "clipboard/registry",
  "clipboard/workspace_comment_paster",
  "clipboard",
  "common",
  "component_manager",
  "config",
  "connection",
  "connection_checker",
  "connection_db",
  "connection_type",
  "constants",
  "contextmenu",
  "contextmenu_items",
  "contextmenu_registry",
  "css",
  "events/events",
  "events/events_abstract",
  "events/events_block_base",
  "events/events_block_change",
  "events/events_block_create",
  "events/events_block_delete",
  "events/events_block_drag",
  "events/events_block_field_intermediate_change",
  "events/events_block_move",
  "events/events_bubble_open",
  "events/events_click",
  "events/events_comment_base",
  "events/events_comment_change",
  "events/events_comment_create",
  "events/events_comment_delete",
  "events/events_comment_move",
  "events/events_marker_move",
  "events/events_selected",
  "events/events_theme_change",
  "events/events_toolbox_item_select",
  "events/events_trashcan_open",
  "events/events_ui_base",
  "events/events_var_base",
  "events/events_var_create",
  "events/events_var_delete",
  "events/events_var_rename",
  "events/events_viewport",
  "events/utils",
  "events/workspace_events",
  "icons",
  "icons/comment_icon",
  "icons/exceptions",
  "icons/icon",
  "icons/icon_types",
  "icons/mutator_icon",
  "icons/registry",
  "icons/warning_icon",
  "inputs",
  "inputs/align",
  "inputs/dummy_input",
  "inputs/end_row_input",
  "inputs/input",
  "inputs/input_types",
  "inputs/statement_input",
  "inputs/value_input",
  "inject",
  "internal_constants",
  "interfaces/i_ast_node_location",
  "interfaces/i_ast_node_location_svg",
  "interfaces/i_ast_node_location_with_block",
  "interfaces/i_autohideable",
  "interfaces/i_block_dragger",
  "interfaces/i_bounded_element",
  "interfaces/i_collapsible_toolbox_item",
  "interfaces/i_component",
  "interfaces/i_connection_checker",
  "interfaces/i_contextmenu",
  "interfaces/i_deletable",
  "interfaces/i_delete_area",
  "interfaces/i_draggable",
  "interfaces/i_drag_target",
  "interfaces/i_flyout",
  "interfaces/i_has_bubble",
  "interfaces/i_icon",
  "interfaces/i_keyboard_accessible",
  "interfaces/i_legacy_procedure_blocks",
  "interfaces/i_metrics_manager",
  "interfaces/i_movable",
  "interfaces/i_observable",
  "interfaces/i_parameter_model",
  "interfaces/i_paster",
  "interfaces/i_positionable",
  "interfaces/i_procedure_block",
  "interfaces/i_procedure_map",
  "interfaces/i_procedure_model",
  "interfaces/i_registrable",
  "interfaces/i_rendered_element",
  "interfaces/i_selectable",
  "interfaces/i_selectable_toolbox_item",
  "interfaces/i_serializable",
  "interfaces/i_serializer",
  "interfaces/i_styleable",
  "interfaces/i_toolbox",
  "interfaces/i_toolbox_item",
  "interfaces/i_variable_backed_parameter_model",
  "keyboard_nav/ast_node",
  "keyboard_nav/basic_cursor",
  "keyboard_nav/cursor",
  "keyboard_nav/marker",
  "keyboard_nav/tab_navigate_cursor",
  "renderers/common/block_rendering",
  "renderers/common/constants",
  "renderers/common/drawer",
  # "renderers/common/info",
  "renderers/common/i_path_object",
  # "renderers/common/marker_svg",
  "renderers/common/path_object",
  "renderers/common/renderer",
  "renderers/geras/measurables/inline_input",
  "renderers/geras/measurables/statement_input",
  "renderers/geras/constants",
  "renderers/geras/drawer",
  "renderers/geras/geras",
  "renderers/geras/highlighter",
  "renderers/geras/highlight_constants",
  "renderers/geras/info",
  "renderers/geras/path_object",
  "renderers/geras/renderer",
  "renderers/measurables/base",
  "renderers/measurables/bottom_row",
  "renderers/measurables/connection",
  "renderers/measurables/external_value_input",
  "renderers/measurables/field",
  "renderers/measurables/hat",
  "renderers/measurables/icon",
  "renderers/measurables/inline_input",
  "renderers/measurables/input_connection",
  "renderers/measurables/input_row",
  "renderers/measurables/in_row_spacer",
  "renderers/measurables/jagged_edge",
  "renderers/measurables/next_connection",
  "renderers/measurables/output_connection",
  "renderers/measurables/previous_connection",
  "renderers/measurables/round_corner",
  "renderers/measurables/row",
  "renderers/measurables/spacer_row",
  "renderers/measurables/square_corner",
  "renderers/measurables/statement_input",
  # "renderers/measurables/top_row",
  # "renderers/measurables/types",
  "renderers/minimalist/constants",
  "renderers/minimalist/drawer",
  "renderers/minimalist/info",
  "renderers/minimalist/minimalist",
  "renderers/minimalist/renderer",
  "renderers/thrasos/info",
  "renderers/thrasos/renderer",
  "renderers/thrasos/thrasos",
  "renderers/zelos/measurables/bottom_row",
  "renderers/zelos/measurables/inputs",
  "renderers/zelos/measurables/row_elements",
  "renderers/zelos/measurables/top_row",
  # "renderers/zelos/constants",
  "renderers/zelos/drawer",
  # "renderers/zelos/info",
  "renderers/zelos/marker_svg",
  "renderers/zelos/path_object",
  "renderers/zelos/renderer",
  "renderers/zelos/zelos",
  # "serialization/blocks",
  "serialization/exceptions",
  "serialization/priorities",
  # "serialization/procedures",
  "serialization/registry",
  # "serialization/variables",
  # "serialization/workspaces",
  "theme/classic",
  "theme/themes",
  "theme/zelos",
  # "toolbox/category",
  # "toolbox/collapsible_category",
  # "toolbox/separator",
  # "toolbox/toolbox",
  # "toolbox/toolbox_item",
  "utils/aria",
  "utils/array",
  # "utils/colour",
  "utils/coordinate",
  "utils/deprecation",
  "utils/dom",
  # "utils/idgenerator",
  "utils/keycodes",
  "utils/math",
  "utils/metrics",
  "utils/object",
  # "utils/parsing",
  "utils/rect",
  "utils/size",
  # "utils/string",
  "utils/style",
  # "utils/svg", # Problema 1
  # "utils/svg_math",
  "utils/svg_paths",
  # "utils/toolbox",
  "utils/useragent",
  # "utils/xml",
  "delete_area",
  "dialog",
  "drag_target",
  # "dropdowndiv",
  # "extensions",
  # "field",
  # "field_angle",
  "field_checkbox",
  # "field_colour",
  # "field_dropdown",
  "field_image",
  # "field_input",
  # "field_label",
  "field_label_serializable",
  "field_multilineinput",
  "field_number",
  # "field_registry",
  "field_textinput",
  "field_variable",
  "flyout_base",
  # "flyout_button",
  "flyout_horizontal",
  # "flyout_metrics_manager",
  "flyout_vertical",
  # "generator",
  # "gesture",
  "grid",
  "insertion_marker_manager",
  "layers",
  "layer_manager",
  # "main",
  "marker_manager",
  "menu",
  "menuitem",
  "metrics_manager",
  "msg",
  # "names",
  "observable_procedure_map",
  "options",
  "positionable_helpers",
  # "procedures",
  # "registry",
  "rendered_connection",
  # "render_management",
  "scrollbar",
  "scrollbar_pair",
  "serialization",
  "shortcut_items",
  # "shortcut_registry",
  "sprites",
  "theme",
  "theme_manager",
  # "tooltip",
  # "touch",
  # "trashcan",
  "utils",
  # "variables",
  "variables_dynamic",
  "variable_map",
  "variable_model",
  "widgetdiv",
  # "workspace",
  # "workspace_audio",
  # "workspace_comment",
  "workspace_comment_svg",
  "workspace_dragger",
  # "workspace_svg",
  # "xml",
  "zoom_controls"
]

def main():
  if len(sys.argv) == 1:
    Boom("No me pasaste ningún archivo")
  nombreArchivo = sys.argv[1]
  verb = True
  archivos = [nombreArchivo]
  if nombreArchivo == "TEST":
    verb = False
    archivos = map(lambda x : f"../../blockly/core/{x}.ts", archivosTest)
  for nombreArchivo in archivos:
    if not existeArchivo_Acá(nombreArchivo):
      Boom("No existe el archivo " + nombreArchivo)
    parsearArchivo(nombreArchivo, verb)

def parsearArchivo(nombreArchivo, verb=True):
  if verb:
    print(nombreArchivo)
  contenido = contenidoDe_(nombreArchivo)
  tokens = tokenizar(contenido)
  # mostrarTokens(tokens)
  ast = parsear(contenido)
  # mostrarAST(ast)
  z = ""
  for a in ast.declaraciones:
    z += a.restore()
  if eq_string(contenido, z):
    if verb:
      print("Restauración exitosa")
  else:
    if not verb:
      print(nombreArchivo)
    print("Falló la restauración")
    mostrarDiff(contenido, z)

if __name__ == '__main__':
  main()