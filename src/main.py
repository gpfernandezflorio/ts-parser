import sys
from bibpy.base import Boom
from bibpy.archivos import contenidoDe_, existeArchivo_Acá
from parser import tokenizar, parsear, mostrarAST, mostrarTokens, mostrarDiff, eq_string

archivosTest = [
  "../../blockly/core/any_aliases.ts",
  # "../../blockly/core/block.ts",
  # "../../blockly/core/block_animation.ts",
  "../../blockly/core/block_dragger.ts",
  # "../../blockly/core/block_svg.ts",
  "../../blockly/core/blockly.ts",
  "../../blockly/core/blockly_options.ts",
  "../../blockly/core/blocks.ts",
  # "../../blockly/core/browser_events.ts",
  "../../blockly/core/bubble_dragger.ts",
  "../../blockly/core/bubbles/bubble.ts",
  "../../blockly/core/bubbles/mini_workspace_bubble.ts",
  "../../blockly/core/bubbles/text_bubble.ts",
  "../../blockly/core/bubbles/textinput_bubble.ts",
  "../../blockly/core/bubbles.ts",
  "../../blockly/core/bump_objects.ts",
  "../../blockly/core/clipboard/block_paster.ts",
  "../../blockly/core/clipboard/registry.ts",
  "../../blockly/core/clipboard/workspace_comment_paster.ts",
  # "../../blockly/core/clipboard.ts",
  # "../../blockly/core/common.ts",
  # "../../blockly/core/component_manager.ts",
  "../../blockly/core/config.ts",
  # "../../blockly/core/connection.ts",
  "../../blockly/core/connection_checker.ts",
  # "../../blockly/core/connection_db.ts",
  "../../blockly/core/connection_type.ts",
  "../../blockly/core/constants.ts",
  # "../../blockly/core/context_menu.ts",
  # "../../blockly/core/context_menu_items.ts",
  # "../../blockly/core/context_menu_registry.ts",
  # "../../blockly/core/css.ts",
  "../../blockly/core/events/events.ts",
  "../../blockly/core/events/events_abstract.ts",
  "../../blockly/core/events/events_block_base.ts",
  "../../blockly/core/events/events_block_change.ts",
  "../../blockly/core/events/events_block_create.ts",
  "../../blockly/core/events/events_block_delete.ts",
  "../../blockly/core/events/events_block_drag.ts",
  "../../blockly/core/events/events_block_field_intermediate_change.ts",
  "../../blockly/core/events/events_block_move.ts",
  "../../blockly/core/events/events_bubble_open.ts",
  "../../blockly/core/events/events_click.ts",
  "../../blockly/core/events/events_comment_base.ts",
  "../../blockly/core/events/events_comment_change.ts",
  "../../blockly/core/events/events_comment_create.ts",
  "../../blockly/core/events/events_comment_delete.ts",
  "../../blockly/core/events/events_comment_move.ts",
  "../../blockly/core/events/events_marker_move.ts",
  "../../blockly/core/events/events_selected.ts",
  "../../blockly/core/events/events_theme_change.ts",
  "../../blockly/core/events/events_toolbox_item_select.ts",
  "../../blockly/core/events/events_trashcan_open.ts",
  "../../blockly/core/events/events_ui_base.ts",
  "../../blockly/core/events/events_var_base.ts",
  "../../blockly/core/events/events_var_create.ts",
  "../../blockly/core/events/events_var_delete.ts",
  "../../blockly/core/events/events_var_rename.ts",
  "../../blockly/core/events/events_viewport.ts",
  "../../blockly/core/events/utils.ts",
  "../../blockly/core/events/workspace_events.ts",
  "../../blockly/core/icons.ts",
  "../../blockly/core/icons/comment_icon.ts",
  "../../blockly/core/icons/exceptions.ts",
  "../../blockly/core/icons/icon.ts",
  "../../blockly/core/icons/icon_types.ts",
  "../../blockly/core/icons/mutator_icon.ts",
  "../../blockly/core/icons/registry.ts",
  "../../blockly/core/icons/warning_icon.ts",
  "../../blockly/core/inputs.ts",
  "../../blockly/core/inputs/align.ts",
  "../../blockly/core/inputs/dummy_input.ts",
  "../../blockly/core/inputs/end_row_input.ts",
  "../../blockly/core/inputs/input.ts",
  "../../blockly/core/inputs/input_types.ts",
  "../../blockly/core/inputs/statement_input.ts",
  "../../blockly/core/inputs/value_input.ts",
  "../../blockly/core/inject.ts",
  "../../blockly/core/internal_constants.ts"
]

def main():
  if len(sys.argv) == 1:
    Boom("No me pasaste ningún archivo")
  nombreArchivo = sys.argv[1]
  archivos = [nombreArchivo]
  if nombreArchivo == "TEST":
    archivos = archivosTest
  for nombreArchivo in archivos:
    if not existeArchivo_Acá(nombreArchivo):
      Boom("No existe el archivo " + nombreArchivo)
    parsearArchivo(nombreArchivo)

def parsearArchivo(nombreArchivo):
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
    print("Restauración exitosa")
  else:
    print("Falló la restauración")
    mostrarDiff(contenido, z)

if __name__ == '__main__':
  main()