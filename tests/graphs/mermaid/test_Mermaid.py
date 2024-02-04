from unittest import TestCase

from osbot_utils.graphs.mermaid.configs.Mermaid__Edge__Config import Mermaid__Edge__Config
from osbot_utils.graphs.mgraph.MGraph__Edge import MGraph__Edge
from osbot_utils.helpers.trace.Trace_Call import trace_calls
from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid__Edge import Mermaid__Edge
from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node, Mermaid__Node__Config
from osbot_utils.graphs.mgraph.MGraph__Node     import MGraph__Node
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import type_mro, obj_data
from osbot_utils.utils.Str                      import str_dedent
from osbot_utils.graphs.mermaid.Mermaid         import Mermaid, Diagram__Direction, Diagram__Type

class test_Mermaid(TestCase):

    def setUp(self):
        self.mermaid = Mermaid()


    def test__init__(self):

        with self.mermaid as _:
            expected_vars = {'logger'           : _.logger              ,
                             'graph'            : _.graph               ,
                             'renderer'         : _.renderer            }
            assert _.__locals__() == expected_vars
            assert _.logger  .logger_name        == 'Python_Logger__Mermaid'
            assert _.logger  .__class__.__name__ == 'Python_Logger'
            assert _.graph   .__class__.__name__ == 'Mermaid__Graph'
            assert _.renderer.__class__.__name__ == 'Mermaid__Renderer'




    def test_config(self):
        assert self.mermaid.renderer.config.add_nodes is True


    def test_set_direction(self):
        with self.mermaid as _:
            assert _.renderer is not None
            #assert _.set_direction(Diagram__Direction.LR) is _
            #assert _.renderer.diagram_direction == Diagram__Direction.LR


    #@trace_calls(contains=['mermaid'])         # this was the code that was triggering the bug
    # todo, move into separate test just focused on the use cases
    def test_use_case_1(self):
        expected_code = """
                            flowchart LR
                                id
                        """
        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='id').show_label(False)

            assert _.code().strip() == str_dedent(expected_code)











# example = """
# flowchart TD
#     A[Christmas] -->|Get money| B(Go shopping)
#     B --> C{Let me think}
#     C -->|One| D[Laptop]
#     C -->|Two| E[iPhone]
#     C -->|Three| F[fa:fa-car Car]
#
# """
#             other_examples = """
# xychart-beta
#     title "Sales Revenue"
#     x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
#     y-axis "Revenue (in $)" 4000 --> 11000
#     bar [1000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
#     line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
#
# mindmap
#   root((mindmap))
#     Origins
#
#       Long history
#       ::icon(fa fa-book)
#       Popularisation
#         British popular psychology author Tony Buzan
#     Research
#       On effectivness<br/>and features
#       On Automatic creation
#         Uses
#             Creative techniques
#             Strategic planning
#             Argument mapping
#     Tools
#       Pen and paper
#       Mermaid
# journey
#     title My working day
#     section Go to work
#       Make tea: 5: Me
#       Go upstairs: 3: Me
#       Do work: 1: Me, Cat
#     section Go home
#       Go downstairs: 5: Me
#       Sit down: 3: Me
# gantt
#     title A Gantt Diagram
#     dateFormat  YYYY-MM-DD
#     section Section
#     A task           :a1, 2014-01-01, 30d
#     Another task     :after a1  , 20d
#     section Another
#     Task in sec      :2014-01-12  , 12d
#     another task      : 24d
# erDiagram
#     CUSTOMER }|..|{ DELIVERY-ADDRESS : has
#     CUSTOMER ||--o{ ORDER : places
#     CUSTOMER ||--o{ INVOICE : "liable for"
#     DELIVERY-ADDRESS ||--o{ ORDER : receives
#     INVOICE ||--|{ ORDER : covers
#     ORDER ||--|{ ORDER-ITEM : includes
#     PRODUCT-CATEGORY ||--|{ PRODUCT : contains
#     PRODUCT ||--o{ ORDER-ITEM : "ordered in"
# stateDiagram-v2
#     [*] --> Still
#     Still --> [*]
#     Still --> Moving
#     Moving --> Still
#     Moving --> Crash
#     Crash --> [*]
# classDiagram
#     Animal <|-- Duck
#     Animal <|-- Fish
#     Animal <|-- Zebra
#     Animal : +int age
#     Animal : +String gender
#     Animal: +isMammal()
#     Animal: +mate()
#     class Duck{
#       +String beakColor
#       +swim()
#       +quack()
#     }
#     class Fish{
#       -int sizeInFeet
#       -canEat()
#     }
#     class Zebra{
#       +bool is_wild
#       +run()
#     }
# flowchart TD
#    A[Christmas] -->|Get money| B(Go shopping)
#    B --> C{Let me think}
#    C -->|One| D[Laptop]
#    C -->|Two| E[iPhone]
#    C -->|Three| F[fa:fa-car Car]
#
# gitGraph LR:
#    commit "Ashish"
#    branch newbranch
#    checkout newbranch
#    commit id:"1111"
#    commit tag:"test"
#    checkout main
#    commit type: HIGHLIGHT
#    commit
#    merge newbranch
#    commit
#    branch b2
#    commit tag:"b2 tag"
# sequenceDiagram
#    participant web as Web Browser
#    participant blog as Blog Service
#    participant account as Account Service
#    participant mail as Mail Service
#    participant db as Storage
#
#    Note over web,db: The user must be logged in to submit blog posts
#    web->>+account: Logs in using credentials
#    account->>db: Query stored accounts
#    db->>account: Respond with query result
#
#    alt Credentials not found
#        account->>web: Invalid credentials
#    else Credentials found
#        account->>-web: Successfully logged in
#
#        Note over web,db: When the user is authenticated, they can now submit new posts
#        web->>+blog: Submit new post
#        blog->>db: Store post data
#
#        par Notifications
#            blog--)mail: Send mail to blog subscribers
#            blog--)db: Store in-site notifications
#        and Response
#            blog-->>-web: Successfully posted
#        end
#    end
#
# sequenceDiagram
#     participant Alice
#     participant Bob
#     Alice->>John: Hello John, how are you?
#     loop Healthcheck
#         John->>John: Fight against hypochondria
#     end
#     Note right of John: Rational thoughts<br/>prevail...
#     John-->>Alice: Great!
#     John->>Bob: How about you?
#     Bob-->>John: Jolly good!
# sequenceDiagram
#     loop Daily query
#         Alice->>Bob: Hello Bob, how are you?
#         alt is sick
#             Bob->>Alice: Not so good :(
#         else is well
#             Bob->>Alice: Feeling fresh like a daisy
#         end
#
#         opt Extra response
#             Bob->>Alice: Thanks for asking
#         end
#     end
# graph TB
#    sq[Square shape] --> ci((Circle shape))
#
#    subgraph A
#        od>Odd shape]-- Two line<br/>edge comment --> ro
#        di{Diamond with <br/> line break} -.-> ro(Rounded<br>square<br>shape)
#        di==>ro2(Rounded square shape)
#    end
#
#    %% Notice that no text in shape are added here instead that is appended further down
#    e --> od3>Really long text with linebreak<br>in an Odd shape]
#
#    %% Comments after double percent signs
#    e((Inner / circle<br>and some odd <br>special characters)) --> f(,.?!+-*ز)
#
#    cyr[Cyrillic]-->cyr2((Circle shape Начало));
#
#     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
#     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
#     class sq,e green
#     class di orange
# pie title NETFLIX
#         "Time spent looking for movie" : 90
#         "Time spent watching it" : 10
# sequenceDiagram
#
#    Alice ->> Bob: Hello Bob, how are you?
#    Bob-->>John: How about you John?
#    Bob--x Alice: I am good thanks!
#    Bob-x John: I am good thanks!
#    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.
#
#    Bob-->Alice: Checking with John...
#    Alice->John: Yes... John, how are you?
#
#
#     """

# graph TB
#     classDef bigText font-size:40px,background-color:blue, color:red,padding:1;
#     classDef smallText font-size:5px;
#
#     classDef green fill:#9f6,stroke:#333,stroke-width:2px;
#     classDef orange fill:#f96,stroke:#333,stroke-width:4px;
#
#
#     C["`A formatted text
#         ===========
#         .Emojis and
#         **bold** and
#         *italics*`"]
#
#     A[Node A]
#     B[Node B]
#
#     A --> B
#
#     class A bigText
#     class B smallText
#
#     class C orange
#