import csv
from math import sqrt
from tkinter import filedialog
from Dijkstra import *
from tkinter import *
from PIL import ImageTk
from PIL import Image
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib

matplotlib.use("TkAgg")

root = Tk()
root.title("Shortest Path By Yoni & Ben")
root.iconbitmap("logo.ico")
root.configure(background='#202528')

startup_pic = ImageTk.PhotoImage(Image.open("background.png"))
vertices = []
edges = []
x_vertices = []
y_vertices = []
ed = []
figure1 = Figure()
subplot1 = figure1.add_subplot(111)
toolbarFrame = Frame(master=root)
bar2 = FigureCanvasTkAgg(figure1, root)
ori_x = 0.0
ori_y = 0.0
dest_x = 0.0
dest_y = 0.0
ori_id = 0
dest_id = 0

startup_bg = Label(image=startup_pic, borderwidth=0, width=620, height=500)
startup_bg.grid(row=0, column=1, rowspan=7)


# --------Functions for Buttons-----------#
def style_axes(subplot, figure):
    global bar2
    global toolbarFrame

    subplot.spines['bottom'].set_color("#FEEDDE")
    subplot.spines['top'].set_color("#FEEDDE")
    subplot.spines['right'].set_color("#FEEDDE")
    subplot.spines['left'].set_color("#FEEDDE")
    subplot.tick_params(axis='x', colors="#FEEDDE")
    subplot.tick_params(axis='y', colors="#FEEDDE")
    subplot.yaxis.label.set_color("#FEEDDE")
    subplot.xaxis.label.set_color("#FEEDDE")
    figure.patch.set_color("#202528")
    subplot.set_facecolor("#1A1E20")


def open_vertices():
    root.filename = filedialog.askopenfilename(title="Open Vertices", filetypes=(('csv files', '*.csv'),))
    vertices_csv = root.filename
    vertice(vertices_csv)


def open_edges():
    root.filename = filedialog.askopenfilename(title="Open Edges", filetypes=(('csv files', '*.csv'),))
    edges_csv = root.filename
    edge(edges_csv)


def vertice(vertice_filepath):
    global vertices
    global x_vertices
    global y_vertices
    vertices = []
    with open(vertice_filepath, 'r') as csvfile:
        getvertices = csv.reader(csvfile, delimiter=',')
        for row in getvertices:
            i = 0
            if row[0][0].isdigit() and row[1][0].isdigit():
                vertices.append([float(row[0]), float(row[1])])
                i += 1
    x_vertices = [ver[0] for ver in vertices]
    y_vertices = [ver[1] for ver in vertices]


def edge(edge_filepath):
    global edges
    edges = []
    with open(edge_filepath, 'r') as csvfile:
        getedges = csv.reader(csvfile, delimiter=',')
        for row in getedges:
            i = 0
            if row[0].isdigit() and row[1].isdigit():
                edges.append([int(row[0]), int(row[1])])
                i += 1


def edges_as_reg(vertices_list, edges_list):
    edges_reg = []
    for edg in edges_list:
        edges_reg.append([vertices_list[edg[0]], vertices_list[edg[1]]])
    return edges_reg


def create_charts():
    global figure1
    global x_vertices
    global y_vertices
    global ed
    global subplot1
    global startup_pic
    startup_bg.grid_forget()
    global toolbarFrame
    global bar2

    ed = edges_as_reg(vertices, edges)
    figure1 = Figure()
    subplot1 = figure1.add_subplot(111)

    for line in ed:
        subplot1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], linewidth=3, color="#FEEDDE")
    subplot1.plot(x_vertices, y_vertices, "o", color="#44857D", markersize=6)
    bar2 = FigureCanvasTkAgg(figure1, root)
    bar2.get_tk_widget().grid(row=0, column=1, rowspan=7)
    style_axes(subplot1, figure1)
    toolbarFrame = Frame(master=root)
    toolbarFrame.grid(row=7, column=1)
    toolbar = NavigationToolbar2Tk(bar2, toolbarFrame)
    toolbar.config(background="#FEEDDE")
    toolbar.message_label.config(background="#FEEDDE")


def clear_charts():
    global figure1
    global subplot1
    global x_vertices
    global y_vertices
    global bar2
    global ed
    global toolbarFrame
    bar2.get_tk_widget().grid_forget()
    toolbarFrame.grid_forget()

    ed = edges_as_reg(vertices, edges)
    figure1 = Figure()
    subplot1 = figure1.add_subplot(111)
    for line in ed:
        subplot1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], linewidth=3, color="#FEEDDE")
    subplot1.plot(x_vertices, y_vertices, "o", color="#44857D", markersize=6)
    bar2 = FigureCanvasTkAgg(figure1, root)
    bar2.get_tk_widget().grid(row=0, column=1, rowspan=7)
    style_axes(subplot1, figure1)
    toolbarFrame = Frame(master=root)
    toolbarFrame.grid(row=7, column=1)
    toolbar = NavigationToolbar2Tk(bar2, toolbarFrame)
    toolbar.config(background="#FEEDDE")
    toolbar.message_label.config(background="#FEEDDE")
    toolbar.update()


def press_ori():
    global p
    p = figure1.canvas.mpl_connect('button_press_event', on_click_ori)


def on_click_ori(event):
    global ori_id
    global vertices
    global ori_x
    global ori_y
    global subplot1
    global bar2
    if event.inaxes is not None:
        clear_charts()
        closest = []
        closest = close_points(event.xdata, event.ydata, vertices)
        ori_x = closest[0]
        ori_y = closest[1]
        ori_id = closest[2]
        subplot1.plot(ori_x, ori_y, "o", color="#FE6625", markersize=8)
        bar2 = FigureCanvasTkAgg(figure1, root)
        bar2.get_tk_widget().grid(row=0, column=1, rowspan=7)
        figure1.canvas.mpl_disconnect(p)


def press_dest():
    global p
    p = figure1.canvas.mpl_connect('button_press_event', on_click_dest)


def on_click_dest(event):
    global vertices
    global dest_x
    global dest_y
    global dest_id
    global subplot1
    global bar2
    if event.inaxes is not None:
        clear_charts()
        closest = close_points(event.xdata, event.ydata, vertices)
        dest_x = closest[0]
        dest_y = closest[1]
        dest_id = closest[2]

        subplot1.plot(ori_x, ori_y, "o", color="#FE6625", markersize=8)
        subplot1.plot(dest_x, dest_y, "o", color="#FB9334", markersize=8)
        bar2 = FigureCanvasTkAgg(figure1, root)
        bar2.get_tk_widget().grid(row=0, column=1, rowspan=7)
        figure1.canvas.mpl_disconnect(p)


def close_points(x, y, pnts):
    closest_point = []
    min_distance = (sqrt((x - pnts[0][0]) ** 2 + (y - pnts[0][1]) ** 2))
    current_distance = 0.0
    closest_point = [pnts[0][0], pnts[0][1], 0]

    for pnt in pnts:
        current_distance = (sqrt((x - pnt[0]) ** 2 + (y - pnt[1]) ** 2))

        if current_distance < min_distance:
            min_distance = current_distance
            closest_point = [pnt[0], pnt[1], pnts.index(pnt)]
    # print("min dist: ", min_distance)
    return closest_point


def calc_path():
    global vertices
    global edges
    global ori_id
    global dest_id
    global subplot1
    global bar2
    graph = Dijkstra(vertices, edges)
    matrix = graph.build_adj_matrix()
    calcu_path = [int(pnt) for pnt in graph.find_shortest_route(ori_id, dest_id, matrix)]
    path_points_xy = path_to_xy(calcu_path, vertices)
    path_edges_xy = path_to_edge_xy(path_points_xy)
    x_vertices_path = [ver[0] for ver in path_points_xy]
    y_vertices_path = [ver[1] for ver in path_points_xy]
    for path_line in path_edges_xy:
        subplot1.plot([path_line[0][0], path_line[1][0]], [path_line[0][1], path_line[1][1]], color="#003D59",
                      linewidth=5)
    subplot1.plot(x_vertices_path, y_vertices_path, "o", markersize=9, color="#C00000")
    bar2 = FigureCanvasTkAgg(figure1, root)
    bar2.get_tk_widget().grid(row=0, column=1, rowspan=7)


def path_to_xy(pathlist, vertices_list):
    pathxy = []
    for i in pathlist:
        pathxy.append([vertices_list[i][0], vertices_list[i][1]])
    return pathxy


def path_to_edge_xy(xypathlist):
    edgexy = []
    for i in range(len(xypathlist) - 1):
        edgexy.append([xypathlist[i], xypathlist[i + 1]])
    return edgexy


def end_program():
    global figure1
    global subplot1
    plt.close(figure1)
    root.quit()


button1 = Button(root, text='📁 | Upload Vertices File', fg="#FEEDDE", bg="#44857D", font=('Mitr', 10),
                 command=open_vertices)
button1.grid(row=0, column=0, sticky=W + E + N + S)

button2 = Button(root, text='📁 | Upload Edges File', fg="#FEEDDE", bg="#167070", font=('Mitr', 10), command=open_edges)
button2.grid(row=1, column=0, sticky=W + E + N + S)

button3 = Button(root, text='🗺️ | Draw', fg="#FEEDDE", bg="#1C909C", command=create_charts, font=('Mitr', 10))
button3.grid(row=2, column=0, sticky=W + E + N + S)

button4 = Button(root, text='📍 | Select Origin Point', fg="#FEEDDE", bg="#FE6625",
                 font=('Mitr', 10), command=press_ori)
button4.grid(row=3, column=0, sticky=W + E + N + S)

button5 = Button(root, text='📍 | Select Destination Point', fg="#FEEDDE", bg="#FB9334",
                 font=('Mitr', 10), command=press_dest)
button5.grid(row=4, column=0, sticky=W + E + N + S)

button6 = Button(root, text='📈 | Calculate Route', fg="#FEEDDE", bg="#003D59", font=('Mitr', 10), command=calc_path)
button6.grid(row=5, column=0, sticky=W + E + N + S)

button7 = Button(root, text='🎇 | Clear Route', command=clear_charts, fg="#FEEDDE", bg="#414A4F", font=('Mitr', 10))
button7.grid(row=6, column=0, sticky=W + E + N + S)

button8 = Button(root, text='👋 | Quit', command=end_program, bg="#001221", fg="#FEEDDE",
                 font=('Mitr', 10))
button8.grid(row=7, column=0, sticky=W + E + N + S)

root.mainloop()

# TODO remove ghost plot
