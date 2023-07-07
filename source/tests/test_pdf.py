import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Create a PDF file
with PdfPages('my_plots.pdf') as pdf:

    # Create the first plot
    fig1, ax1 = plt.subplots()
    ax1.plot([1, 2, 3, 4], [1, 4, 2, 3])
    ax1.set_title('Plot 1')

    # Add the first plot to the PDF
    pdf.savefig(fig1)

    # Create the second plot
    fig2, ax2 = plt.subplots()
    ax2.plot([1, 2, 3, 4], [4, 2, 3, 1])
    ax2.set_title('Plot 2')

    # Add the second plot to the PDF
    pdf.savefig(fig2)

    # Create the third plot
    fig3, ax3 = plt.subplots()
    ax3.plot([1, 2, 3, 4], [2, 3, 1, 4])
    ax3.set_title('Plot 3')

    # Add the third plot to the PDF
    pdf.savefig(fig3)

    # Create the fourth plot
    fig4, ax4 = plt.subplots()
    ax4.plot([1, 2, 3, 4], [3, 1, 4, 2])
    ax4.set_title('Plot 4')

    # Add the fourth plot to the PDF
    pdf.savefig(fig4)

    # Close the PDF file
    #pdf.close()
