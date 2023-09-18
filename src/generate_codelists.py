from pathlib import Path
import click
import pandas as pd
import json
#from csvcubed import ensure_no_uri_safe_conflicts


@click.command()
@click.argument("codelist_csv", type=click.Path(exists=True, path_type=Path))
@click.option("--template", type=click.Path(exists=True, path_type=Path))
def generate_codelist(codelist_csv: Path(), template: Path()) -> None:
    if template is None:
        template = "src/codelist_template.json"

    df = pd.read_csv(codelist_csv)
    codelist_groupby_df = df.groupby(by="codelist_name")

    for name, group in codelist_groupby_df:
        for row in group.itertuples():
            title = row.codelist_name

        with open(template) as f:
            codelist_template = json.load(f)

        group = group[["label", "notation", "description"]]

        group = group.fillna("")

        codelist = json.loads(group.to_json(orient="records"))

        codelist_template["concepts"] = codelist
        codelist_template["title"] = title

        file_name = title.lower().replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")

        with open(f"Codelists/{file_name}.json", "w") as f:
            json.dump(codelist_template, f, indent=4)

if __name__ == "__main__":
    generate_codelist()