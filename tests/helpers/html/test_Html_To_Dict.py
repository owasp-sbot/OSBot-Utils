from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Html import Dict_To_Html
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set


class test_Html_To_Dict(TestCase):

    def test_convert(self):
        html = """
<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Simple Bootstrap 5 Webpage</title>
      <!-- Bootstrap CSS -->
      <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Qt9Hug5NfnQDGMoaQYXN1+PiQvda2v7deG6T2EFAv6PE3ZZdT8iV3J3JZK9Fiq1k" crossorigin="anonymous"/>
    </head>
    <body>
    
      <!-- Navigation -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Webpage Name</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Features</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Pricing</a>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      
      <!-- Jumbotron / Hero -->
      <div class="p-5 mb-4 bg-light rounded-3">
        <div class="container-fluid py-5">
          <h1 class="display-5 fw-bold">Welcome to Our Website!</h1>
          <p class="col-md-8 fs-4">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
          <button class="btn btn-primary btn-lg" type="button">Example button</button>
        </div>
      </div>
    
      <!-- Footer -->
      <footer class="py-3 my-4">
        <ul class="nav justify-content-center border-bottom pb-3 mb-3">
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Home</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Features</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Pricing</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">FAQs</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">About</a></li>
        </ul>
        <p class="text-center text-muted">© 2023 Company, Inc</p>
      </footer>
    
      <!-- Bootstrap JS -->
      <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js" integrity="sha384-kQtW33rZJAHjy8F/xlNY8M3KD6FpD3FqJ8sLI+4zl5S5MkP40gOhB2tHRzVyN7bR" crossorigin="anonymous"></script>
    </body>
</html>
    """
        html_parser_1    = Html_To_Dict(html)
        root_1           = html_parser_1.convert()
        lines_1          = html_parser_1.print(just_return_lines=True)
        dict_to_html_1   = Dict_To_Html(root_1)

        html_from_dict_1 = dict_to_html_1.convert()
        html_parser_2    = Html_To_Dict(html_from_dict_1)
        root_2           =  html_parser_2.convert()
        lines_2 = html_parser_2.print(just_return_lines=True)

        assert root_1  == root_2
        assert lines_1 == lines_2

        assert lines_1 == [  'html (lang="en")',
                             '    ├── head\n'
                             '    │   ├── meta (charset="UTF-8")\n'
                             '    │   ├── meta (name="viewport" content="width=device-width, initial-scale=1.0")\n'
                             '    │   ├── title\n'
                             '    │   └── link (href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" '
                                               'rel="stylesheet" '
                                               'integrity="sha384-Qt9Hug5NfnQDGMoaQYXN1+PiQvda2v7deG6T2EFAv6PE3ZZdT8iV3J3JZK9Fiq1k" '
                                               'crossorigin="anonymous")',
                             '    └── body\n'
                             '        ├── nav (class="navbar navbar-expand-lg navbar-dark bg-dark")\n'
                             '        │   └── div (class="container-fluid")\n'
                             '        │       ├── a (class="navbar-brand" href="#")\n'
                             '        │       ├── button (class="navbar-toggler" type="button" '
                                                         'data-bs-toggle="collapse" data-bs-target="#navbarNav" '
                                                         'aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle '
                                                         'navigation")\n'
                             '        │       │   └── span (class="navbar-toggler-icon")\n'
                             '        │       └── div (class="collapse navbar-collapse" id="navbarNav")\n'
                             '        │           └── ul (class="navbar-nav")\n'
                             '        │               ├── li (class="nav-item")\n'
                             '        │               │   └── a (class="nav-link active" aria-current="page" href="#")\n'
                             '        │               ├── li (class="nav-item")\n'
                             '        │               │   └── a (class="nav-link" href="#")\n'
                             '        │               ├── li (class="nav-item")\n'
                             '        │               │   └── a (class="nav-link" href="#")\n'
                             '        │               └── li (class="nav-item")\n'
                             '        │                   └── a (class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true")\n'
                             '        ├── div (class="p-5 mb-4 bg-light rounded-3")\n'
                             '        │   └── div (class="container-fluid py-5")\n'
                             '        │       ├── h1 (class="display-5 fw-bold")\n'
                             '        │       ├── p (class="col-md-8 fs-4")\n'
                             '        │       └── button (class="btn btn-primary btn-lg" type="button")\n'
                             '        ├── footer (class="py-3 my-4")\n'
                             '        │   ├── ul (class="nav justify-content-center border-bottom pb-3 mb-3")\n'
                             '        │   │   ├── li (class="nav-item")\n'
                             '        │   │   │   └── a (href="#" class="nav-link px-2 text-muted")\n'
                             '        │   │   ├── li (class="nav-item")\n'
                             '        │   │   │   └── a (href="#" class="nav-link px-2 text-muted")\n'
                             '        │   │   ├── li (class="nav-item")\n'
                             '        │   │   │   └── a (href="#" class="nav-link px-2 text-muted")\n'
                             '        │   │   ├── li (class="nav-item")\n'
                             '        │   │   │   └── a (href="#" class="nav-link px-2 text-muted")\n'
                             '        │   │   └── li (class="nav-item")\n'
                             '        │   │       └── a (href="#" class="nav-link px-2 text-muted")\n'
                             '        │   └── p (class="text-center text-muted")\n'
                             '        └── script (src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js" '
                                                 'integrity="sha384-kQtW33rZJAHjy8F/xlNY8M3KD6FpD3FqJ8sLI+4zl5S5MkP40gOhB2tHRzVyN7bR" '
                                                 'crossorigin="anonymous")']
