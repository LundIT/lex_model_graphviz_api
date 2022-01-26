
from graphviz import Digraph

def body_to_html_table(class_name, body):
    table = f"<" \
            f'<TABLE HREF="www.google.com">' \
            f"<TR><TD>{class_name}</TD></TR>" \
            f"<TR><TD>" \
            f"<TABLE>"
    for item in body:
        table += f"<TR>"
        for key in item.keys():
            table += f"<TD>{item[key]}</TD>"
        table += f"</TR>"
    table += f"</TABLE>" \
             f"</TD></TR></TABLE>>"
    return table

def convert_json_to_graphviz_svg(json:dict):
    graph = Digraph(comment=f"Class Visualization", engine='dot')
    graph.attr('graph', splines='ortho')
    for class_name in json.keys():
        graph.node(class_name, label=body_to_html_table(class_name, json[class_name]), style='filled', fillcolor='snow')
        foreign_keys = [x['to'] for x in json[class_name] if x['data_type']=='ForeignKey']
        for fk in foreign_keys:
            graph.edge(class_name, fk)

    graph.format = 'svg'
    svg_string = graph.pipe(encoding='utf-8')
    return svg_string
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json = {
        'class1': [
            {'column_name': 'id', 'data_type': 'FloatField', 'default_value': None},
            {'column_name': 'c1', 'data_type': 'FloatField', 'default_value': 0},
            {'column_name': 'c2', 'data_type': 'XLSXField', 'default_value': None},
            ],
        'class2': [
            {'column_name': 'id', 'data_type': 'FloatField', 'default_value': None},
            {'column_name': 'c3', 'data_type': 'ForeignKey', 'default_value': None, 'to': 'class1', 'on_delete': 'CASCADE'},
        ]
    }
    svg_string = convert_json_to_graphviz_svg(json)
    print(svg_string)
