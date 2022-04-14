import pins
import warnings

def _choose_version(df):
    if 'active' in df.columns:
        version = df.active[0]
    elif 'created' in df.columns: 
        version_desc = df.sort_values(by='created', ascending=False)
        version = version_desc.version[0]
    else:
        version = df.version[0]
        warnings.warn(
            f"""Pinned vetiver model has no active version and no datetime on versions,
              Do you need to check your pinned model?
              Using version {version}"""
        )
    return version

def _glue_required_pkgs(required_pkgs: list):
    load_required_pkgs = ""
    if required_pkgs:
        for pkg in required_pkgs:
            load_required_pkgs = load_required_pkgs + f"import {pkg}\n"

    return load_required_pkgs

def vetiver_write_app(board: pins.BaseBoard, pin_name: str,
              version=None, file = "app.py"):
    """Write VetiverAPI app to a file

    Attributes
    ----------
    vetiver_api :  VetiverAPI
        API to be written
    name : string
        name of file
    """

    if board.versioned:
        if not version:
            version = board.pin_versions(pin_name)
            version = _choose_version(version)
        pin_read = f"v = vetiver.vetiver_pin_read(b, {repr(pin_name)}, version = {repr(version)})"
        
    else:
        pin_read = f"v = vetiver.vetiver_pin_read(b, {repr(pin_name)})"

    infra_pkgs = ['vetiver', 'pins']


    load_board = pins.board_deparse(board)
    
    f = open(file, "x")

    app = f"""{_glue_required_pkgs(infra_pkgs)}

b = pins.{load_board}
{pin_read}

vetiver_api = vetiver.VetiverAPI(v)
app = vetiver_api.app
"""

    f.write(app)
