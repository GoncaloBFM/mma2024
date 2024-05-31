import dash_bootstrap_components as dbc


def create_help_popup():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("How to use")),
            dbc.ModalBody("This is the content of the modal"),
        ],
        id="help-popup",
        is_open=False,
    )
