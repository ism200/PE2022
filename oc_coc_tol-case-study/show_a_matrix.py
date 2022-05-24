"""Quick and dirty implementation to show all a-matrixes of a result."""

from __future__ import annotations

from glotaran.project import Result
from glotaran.utils.ipython import MarkdownStr
from tabulate import tabulate


def show_a_matrix(result: Result, heading_offset: int = 2) -> MarkdownStr:
    """Return a markdownstr showing all a-matrixes of the result split by name and dataset."""
    heading_prefix = heading_offset * "#"
    output_str = f"#{heading_prefix} A-Matrixes"

    for dataset_name in result.data:

        output_str += f"\n\n##{heading_prefix} {dataset_name}:\n"

        a_matrix_names = list(
            filter(
                lambda var_name: var_name.startswith("a_matrix_"),
                result.data[dataset_name].data_vars,
            )
        )

        for a_matrix_name in a_matrix_names:

            a_matrix = result.data[dataset_name][a_matrix_name]

            mc_suffix = a_matrix_name.replace("a_matrix_", "")

            header = ["species<br>initial concentration<br>lifetime↓"] + [
                f"{sp}<br>{ic}<br>&nbsp;"
                for sp, ic in zip(
                    a_matrix.coords[f"species_{mc_suffix}"].values,
                    a_matrix.coords[f"initial_concentration_{mc_suffix}"].values,
                )
            ]

            data = [
                [lifetime, *amps]
                for lifetime, amps in zip(
                    a_matrix.coords[f"lifetime_{mc_suffix}"].values, a_matrix.values
                )
            ]

            output_str += f"\n\n###{heading_prefix} {a_matrix_name}:\n\n"

            output_str += (
                tabulate(data, headers=header, showindex=False, tablefmt="unsafehtml")
                .replace(" 0 ", "   ")
                .replace(" 0<", "  <")
            )

    return MarkdownStr(output_str)
