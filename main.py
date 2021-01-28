import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons

from controller import *


def view():
    
    # fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    
    # axes style
    ax.set_title('B-Spline-Curves')
    ax.set_xlim(1, 10)
    ax.set_ylim(1, 24)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

    # fig layout
    plt.text(10.3, 18, "User Tips:", fontfamily='fantasy', fontstyle='italic',
             fontsize='large', fontweight='roman', color='r', backgroundcolor='#87CEEB',  # skyblue
             bbox=dict(boxstyle="round", fc='#87CEEB'), rasterized='True'
             )
    plt.text(10.5, 11, "Add  point: $Mouse-Right$\n"
                       "Drag point: $Mouse-Left$\n"
                       "Hide Line: h / H\nExit: q / Q\n",
             fontfamily='serif', fontstyle='oblique', fontsize='medium', color='#000080'
             )
    
    # add new line button, input textbox and radio button
    addlinebtn = fig.add_axes([0.75, 0.22, 0.2, 0.075])
    inputbox = fig.add_axes([0.85, 0.12, 0.1, 0.07])
    rax = fig.add_axes([0.75, 0.32, 0.2, 0.12])
    
    # button click
    btncallback = CreatLine(ax)
    binsert = Button(addlinebtn, 'New Line', color='#00BFFF')
    binsert.on_clicked(btncallback.createnewline)
    
    # input submit
    input_text = TextBox(inputbox, "Degree : ")
    input_text.on_submit(change_degree)
    input_text.set_val("3")
    
    # radio callback
    radio = RadioButtons(rax, ("Uniform", "Clamped"))
    radio.on_clicked(change_type)

    # add first line
    CreatLine(ax).createnewline(event=None)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.02), fontsize='medium', shadow='True')

    plt.show()


if __name__ == '__main__':
    view()
