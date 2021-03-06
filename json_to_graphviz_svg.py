from graphviz import Digraph
from example_jsons import *

# this function takes a set of member_variables (body) and creates a HTML-Like label for graphviz
def body_to_html_table(class_name, body):
    table = f"<" \
            f'<TABLE>' \
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

#this function takes a json defining the structure of a model graph and turns it into an svg string of the graph
def convert_json_to_graphviz_svg(json:dict):
    graph = Digraph(comment=f"Class Visualization", engine='dot')
    graph.attr('graph', splines='ortho')
    for model in json['models']:
        graph.node(model['class']['name'], label=body_to_html_table(model['class']['name'], model['class']['columns']), style='filled', fillcolor='snow')
        foreign_keys = [x['to'] for x in model['class']['columns'] if x['data_type']=='ForeignKey']
        for fk in foreign_keys:
            for model_name in json['models']:
                if model_name['class']['name'] == fk:
                    graph.edge(model['class']['name'], model_name['class']['name'])
    graph.format = 'svg'
    svg_string = graph.pipe(encoding='utf-8')
    return svg_string

if __name__ == '__main__':

    svg_string = convert_json_to_graphviz_svg(input_json_1)
    print(svg_string)
