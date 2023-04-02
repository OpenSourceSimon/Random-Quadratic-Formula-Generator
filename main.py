from flask import Flask, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import random
from sympy import solveset, S
import io
import matplotlib.pyplot as plt
import numpy as np
from sympy import lambdify, symbols
import base64

app = Flask(__name__)


def generate_quadratic_formula():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)

    function_letter = chr(random.randint(102, 122))

    formula = f"{function_letter}(x) = {a}x**2 + {b}x + {c}"

    return formula


def calculate_quadratic_formula(formula):
    a, b = formula.split(" = ")[1].split("x**2 + ")
    c = b.split("x + ")[1]
    b = b.split("x + ")[0]

    x = symbols("x")
    quadratic_formula = f"{a}*{x}**2 + {b}*{x} + {c}"

    solutions = solveset(quadratic_formula, domain=S.Reals)
    if solutions == S.EmptySet:
        return "This formula has no real solutions"

    solutions = [eval(str(solution)) for solution in solutions]
    solutions = [round(solution, 2) for solution in solutions]
    if len(solutions) == 2:
        answer = f"There are two solutions of this formula: x = {solutions[0]} and x = {solutions[1]}"
    elif len(solutions) == 1:
        answer = f"There is one solution of this formula: x = {solutions[0]}"
    else:
        answer = "This formula has no solutions"
    return answer


def create_image(formula):
    font = ImageFont.truetype("arial.ttf", 40)
    text = formula.replace("x**2", "x²")
    text_length = font.getlength(text)

    img = Image.new("RGB", (int(text_length) + 100, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    text = formula.replace("x**2", "x²")
    d.text((50, 20), text, fill=(0, 0, 0), font=font)

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")

    img_tag = base64.b64encode(img_buffer.getvalue()).decode()

    return img_tag


def create_graph(formula):
    a, b = formula.split(" = ")[1].split("x**2 + ")
    c = b.split("x + ")[1]
    b = b.split("x + ")[0]

    x = symbols("x")
    quadratic_formula = f"{a}*{x}**2 + {b}*{x} + {c}"

    f = lambdify(x, quadratic_formula, "numpy")
    x_range = (-10, 10)
    x_vals = np.linspace(x_range[0], x_range[1])
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals)
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Graph of the quadratic formula")

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="jpg")
    my_stringIObytes.seek(0)
    graph = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close()
    return graph


# Route to show the formula and the answer
@app.route("/", methods=["GET"])
def index():
    formula = generate_quadratic_formula()
    answer = calculate_quadratic_formula(formula)
    graph = create_graph(formula)
    img_tag = create_image(formula)

    return render_template(
        "index.html", answer=answer, img_tag=img_tag, answers=answer, graph=graph
    )


@app.route("/api", methods=["GET"])
def api():
    formula = generate_quadratic_formula()
    answer = calculate_quadratic_formula(formula)
    graph = create_graph(formula)
    img_tag = create_image(formula)

    return {
        "formula": formula,
        "answer": answer,
        "graph": graph,
        "img_tag": img_tag,
    }


if __name__ == "__main__":
    app.run(debug=True)
