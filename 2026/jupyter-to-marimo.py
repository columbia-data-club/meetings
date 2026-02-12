import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import datetime as dt
    import math
    import altair

    altair.data_transformers.enable("vegafusion")
    return dt, math, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Move beyond Jupyter Notebooks with Marimo

    12 February 2026<br>
    Moacir P. de Sá Pereira<br>
    [Research Data Services](https://library.columbia.edu/research-teaching/research-data.html)

    Today, we are discussing [Marimo](https://marimo.io/), a tool for building [interactive web notebooks](https://en.wikipedia.org/wiki/Notebook_interface) in Python. Marimo will look and feel a lot like a Jupyter Notebook, but it also has key differences that prompt today’s session. That is, a lot of what will follow will assume a certain familiarity with Jupyter notebooks, but I will not just be comparing the two throughout.

    Jupyter Notebooks have been a boon for expanding access to Python because the notebook model allows for very quick coding and experimentation. It also greatly simplifies teaching Python; Learning Python without a Jupyter Notebook in some ways might be a little like learning R without RStudio. It’s certainly possible, but it is not the best experience, especially for a new learner.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Marimo and Jupyter Comparison

    ### The Cell

    The central innovation of Jupyter notebooks was the focus on using cells to separate code into smaller chunks that could be run in small chunks. This allowed for experimentation and exploration as well as a quick process from thought to execution. Additionally, Jupyter allows for incorporating cells with Markdown prose in them as well as Python code, allowing notebooks to tell an intellectual story, documenting decisions or the way, for example, in an exploratory data analysis environment, that the data was changed around to yield particular insights.

    This process is repeated in Marimo, but with a vital distinction: reactivity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reactivity

    Let's imagine a Jupyter Notebook (this screenshot is actually from a Google Colab notebook):

    ![A screenshot of three Colab cells. Two assign a numerical value to the variable a, and the third assigns to c the value of a + 2 and then prints the value of c](https://i.imgur.com/42NkDLQ.png)

    What happens when we run the third cell, with `print(c)` in it?

    Now, for laughs, let’s make those three cells in Marimo:
    """)
    return


@app.cell
def _():
    a = 2
    return (a,)


@app.cell
def _():
    a = 7
    return (a,)


@app.cell
def _(a):
    c = a + 2
    print(c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We get an error in the second cell, because we are trying to assign a value to a variable that already had a value assigned to it in a different cell.

    In Jupyter, cells can (and often do) overwrite each other and have all sorts of naming clashes, where the last cell to run is the winner. Anyone who has used Jupyter notebooks for a while has probably had the experience of running a cell, then changing the code in it, and then running it again, only to find that the results are different from what they expected because the variable names have been reused in different cells or changed elsewhere.

    In Marimo, on the other hand, a variable can only be set once, because the cells make up a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph). That is, in the background Marimo is deciding what order the cells have to run in so that every cell that depends on another cell is run after the cell it depends on. The cell that defines `c` relies on the cell that defines `a`, because the value of `c` depends on the value of `a`. But if `a` is defined in two different cells, Marimo does not know which one to use, and it throws an error.

    This is because Marimo is __reactive__. Requiring that the cells form a DAG opens up a lot of power in a notebook in terms of its consistency but also in terms of its ordering. Since Marimo builds the DAG behind the scenes, the order of cells is not important.
    """)
    return


@app.cell
def _():
    b = 3
    return (b,)


@app.cell
def _(b, e):
    d = e + b
    print(d)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In terms of interactivity, we have even more flexibility, too. In the above cells, we can see that we’re relying on a variable `e`, that’s defined at the very end of this notebook, but the cell evaluates here with no difficulty. Furthermore, I can edit the value of `b` here, and the value of `d` updates __automatically__, because Marimo understands that a dependency has changed, and it reruns all the downstream cells.

    Incidentally, this behavior is also what makes [Observable Notebooks](https://observablehq.com/) so powerful. Marimo brings these idioms and the power of Observable from JavaScript to Python.
    """)
    return


@app.cell
def _():
    e = 5
    return (e,)


@app.cell(hide_code=True)
def _(f, math, mo):
    mo.md(rf"""
    ### Interactivity

    Because we can reliably predict the order the cells will run in, we can incorporate UI elements to alter values where they make sense in the notebook, not where they have to be so everything executes correctly when we press “Play All.”

    $e^f = {math.exp(f.value):0.3f}\ ;\quad f = {f.value}$
    """)
    return


@app.cell
def _(mo):
    f = mo.ui.slider(1, 9)
    f
    return (f,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Marimo provides [several interactive elements](https://docs.marimo.io/api/inputs/), and we’ll see at least one more later in this notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Notebook Itself

    Jupyter Notebooks are based on the `.ipynb` file format, showing their descent from [iPython](https://en.wikipedia.org/wiki/IPython). The format, however, is not Python. It is, rather, JSON. For example, the Colab Notebook I screenshotted earlier looks like this:

    ```json
    {
      "nbformat": 4,
      "nbformat_minor": 0,
      "metadata": {
        "colab": {
          "provenance": []
        },
        "kernelspec": {
          "name": "python3",
          "display_name": "Python 3"
        },
        "language_info": {
          "name": "python"
        }
      },
      "cells": [
        {
          "cell_type": "code",
          "execution_count": null,
          "metadata": {
            "id": "X6_9-SwguQa4"
          },
          "outputs": [],
          "source": [
            "a = 2"
          ]
        },
        {
          "cell_type": "code",
          "source": [
            "a = 7"
          ],
          "metadata": {
            "id": "_6-Z0i3GuV3M"
          },
          "execution_count": null,
          "outputs": []
        },
        {
          "cell_type": "code",
          "source": [
            "c = a + 2\n",
            "print(c)"
          ],
          "metadata": {
            "id": "QlyHaWn2uZ_r"
          },
          "execution_count": null,
          "outputs": []
        }
      ]
    }
    ```

    If you are using notebooks in a version controlled environment (such as Git), you can see that code review and bug tracking in Git becomes difficult because though the Notebook is _interpreted_ as Python by the Jupyter server, it is not, actually, by itself, Python.

    Here is the equivalent Marimo notebook:

    ```py
    # /// script
    # [tool.marimo.runtime]
    # auto_instantiate = false
    # ///

    import marimo

    __generated_with = "0.19.9"
    app = marimo.App(width="medium")

    @app.cell
    def _():
        import marimo as mo

        return

    @app.cell
    def _():
        a = 2
        return (a,)

    @app.cell
    def _():
        a = 7
        return (a,)

    @app.cell
    def _(a):
        c = a + 2
        print(c)
        return

    if __name__ == "__main__":
        app.run()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If nothing else, the Marimo notebook actually looks like (and executes like) Python, because that is what it is. Instead of an `.ipynb` extension, it has a `.py` extension. The cells are not an array of JavaScript objects, but, rather, a series of functions with the [`@app.cell` decorator](https://docs.marimo.io/api/cell/) .
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Marimo and WASM

    What’s more, because the notebook a self-contained Python script, Marimo lets you export the notebook as a stand-alone web page that leverages [WASM](https://en.wikipedia.org/wiki/WebAssembly) to ship a functional notebook served as a regular webpage. This command:

    ```sh
    uv run marimo export html-wasm jupyter-to-marimo.py -o jupyter-to-marimo --mode edit
    ```

    Produces a folder that holds all the necessary web assets to serve the notebook as a regular webpage. The WASM version of the notebook is fully functional, and it can be shared with anyone, even if they do not have Jupyter (or even Python!) installed on their machine.

    Of course, the WASM version is what you’re currently using on your own computer!
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using Data

    With a general sense of how Marimo works in comparison to Jupyter, now we can move ahead to using Marimo in the context of a regular notebook. In this case, we can do some exploratory data analysis on the [November 2025 NYC Yellow Cab trip data](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet), which we will read with [Polars](https://pola.rs).
    """)
    return


@app.cell
def _():
    taxi_data_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
    return (taxi_data_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Linear Transforms (Pandas Classic)
    """)
    return


@app.cell
def _(pl, taxi_data_url):
    raw_df = pl.read_parquet(taxi_data_url)
    raw_df.head()
    return (raw_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We have some amusing widgets and interactivity even from this basic `.head()` method in Polars. Let’s do even better.
    """)
    return


@app.cell
def _(raw_df):
    raw_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we see all four million rows of the dataframe we downloaded, and we can sort and filter the data as well. First, however, let’s get rid of some of the columns and rename them.
    """)
    return


@app.cell
def _(pl):
    renamed_columns = [
            pl.col("tpep_pickup_datetime").alias("pickup"),
            pl.col("tpep_dropoff_datetime").alias("dropoff"),
            pl.col("passenger_count").alias("passengers"),
            pl.col("trip_distance").alias("distance"),
            pl.col("fare_amount").alias("fare"),
            pl.col("tip_amount").alias("tip"),
            pl.col("total_amount").alias("total")
        ]
    return (renamed_columns,)


@app.cell
def _(raw_df, renamed_columns):
    df = raw_df.select(renamed_columns)
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you’re used to using pandas, you are probably used to having a bunch of lines of code, where each line transforms the dataframe that look something like this:

    ```py
    df = df[df["passengers"] > 0]
    df = df[df["distance"] > 0]
    df = df[df["fare"] > 0]
    df["tip_pct"] = df["tip"] / df["fare"]
    ```

    In Marimo, this will work as long as these reassignments to `df` are all in the same cell. If we broke this apart into multiple cells, however, what will happen? Why?

    One option to fix this is to split up each transformation into its own function.
    """)
    return


@app.cell
def _(df, pl):
    filtered_df = df.filter(
        (pl.col("passengers") > 0) &
        (pl.col("distance") > 0) &
        (pl.col("fare") > 0)
    )
    filtered_df
    return


@app.cell
def _(pl):
    def passengers_above_zero(df):
        return df.filter(pl.col("passengers") > 0)

    return


@app.cell
def _(pl):
    def distance_above_zero(df):
        return df.filter(pl.col("distance") > 0)

    return


@app.cell
def _(pl):
    def fare_above_zero(df):
        return df.filter(pl.col("fare") > 0)

    return


@app.cell
def _(pl):
    def add_tip_pct(df):
        return df.with_columns((pl.col("tip") / pl.col("fare")).alias("tip_pct"))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In pandas, we would then chain these functions together with a series of `pipe()` calls, in what Polars calls “[pipe littering](https://docs.pola.rs/user-guide/migration/pandas/#pipe-littering).” This is inefficient in Polars, because it relies on a linearity that reproduces the linearity of the Jupyter notebook, where everything has to be executed in a specific order so that it may work.

    Part of the power of Polars lies in its [query optimizations in lazy mode](https://docs.pola.rs/user-guide/lazy/optimizations/), so let’s reimagine all of the above using the optimizations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Lazy Transforms (Polars Awesome)
    """)
    return


@app.cell
def _(pl, renamed_columns, taxi_data_url):
    q1 = (
        pl.scan_parquet(taxi_data_url)
        .select(renamed_columns)
        .filter(
            (pl.col("passengers") > 0) &
            (pl.col("distance") > 0) &
            (pl.col("fare") > 0)
        )
        .with_columns((pl.col("tip") / pl.col("fare")).alias("tip_pct"))
    )
    return (q1,)


@app.cell
def _(q1):
    q1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Even better, let’s just look at the taxi rides for Thanksgiving weekend.
    """)
    return


@app.cell
def _(dt, pl, renamed_columns, taxi_data_url):
    q2 = (
        pl.scan_parquet(taxi_data_url)
        .select(renamed_columns)
        .filter(
            pl.col("pickup").is_between(dt.datetime( 2025, 11, 26), dt.datetime(2025, 11, 29))
     &
            (pl.col("passengers") > 0) &
            (pl.col("distance") > 0) &
            (pl.col("fare") > 0)
        )
        .with_columns((pl.col("tip") / pl.col("fare")).alias("tip_pct"))
    )
    q2
    return (q2,)


@app.cell
def _(mo, q2):
    df_good = q2.collect()
    mo.ui.table(df_good)
    return (df_good,)


@app.cell
def _(df_good, mo):
    mo.ui.dataframe(df_good)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
