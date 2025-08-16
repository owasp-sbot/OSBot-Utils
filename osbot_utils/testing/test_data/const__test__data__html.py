TEST__DATA__HTML__SIMPLE =  """
            <html>
                <head>
                    <title>Test Page</title>
                    <link rel="stylesheet" href="/css/main.css">
                    <link rel="shortcut icon" href="/favicon.ico">
                    <meta name="description" content="Test description">
                </head>
                <body>
                    <div id="main">Content</div>
                    <script src="/js/app.js"></script>
                    <script>console.log('inline');</script>
                </body>
            </html>
        """
TEST__DATA__HTML__SWAGGER = """
            <!DOCTYPE html>
            <html>
                <head>
                    <link type="text/css" rel="stylesheet" href="/static/swagger-ui/swagger-ui.css">
                    <link rel="shortcut icon" href="/static/swagger-ui/favicon.png">
                    <title>Fast_API - Swagger UI</title>
                </head>
                <body>
                    <div id="swagger-ui"></div>
                    <script src="/static/swagger-ui/swagger-ui-bundle.js"></script>
                    <script>
                        const ui = SwaggerUIBundle({
                            url: '/openapi.json',
                            "dom_id": "#swagger-ui"
                        })
                    </script>
                </body>
            </html>
        """

TEST__DATA__HTML__MIXED_CONTENT = """
            <div class="container">
                Text before
                <p class="paragraph">Paragraph content</p>
                Text middle
                <span class="highlight">Highlighted</span>
                Text after
            </div>
        """