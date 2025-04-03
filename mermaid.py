# mermaid.py

from graph import build_graph


graph = build_graph()
png_data = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_data)
print("이미지가 'graph.png'로 저장되었습니다.")