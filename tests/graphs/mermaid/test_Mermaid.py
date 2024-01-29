from unittest import TestCase

from osbot_utils.graphs.mgraph.MGraph__Edge import MGraph__Edge
from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid__Edge import Mermaid__Edge
from osbot_utils.graphs.mermaid.Mermaid__Node   import Mermaid__Node
from osbot_utils.graphs.mgraph.MGraph__Node     import MGraph__Node
from osbot_utils.utils.Objects                  import type_mro
from osbot_utils.utils.Str                      import str_dedent
from osbot_utils.graphs.mermaid.Mermaid         import Mermaid, Diagram__Direction, Diagram__Type

class test_Mermaid(TestCase):

    def setUp(self):
        self.mermaid = Mermaid()


    def test__init__(self):

        with self.mermaid as _:
            expected_vars = {'config__add_nodes': True                  ,
                             'diagram_direction': _.diagram_direction   ,
                             'diagram_type'     : _.diagram_type        ,
                             'logger'           : _.logger              ,
                             'mermaid_code'     : []                    ,
                             'graph'            : _.graph               }
            assert _.__locals__() == expected_vars
            assert _.logger.logger_name == 'Python_Logger__Mermaid'


    def test_code(self):
        expected_code = str_dedent("""
                                        flowchart TD
                                            A[Christmas] -->|Get money| B(Go shopping)
                                            B --> C{Let me think}
                                            C -->|One| D[Laptop]
                                            C -->|Two| E[iPhone]
                                            C -->|Three| F[fa:fa-car Car]
                                            """)

        with self.mermaid as _:
            _.set_config__add_nodes(False)
            _.set_direction(Diagram__Direction.TD)
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(label='Christmas'    , key='A').wrap_with_quotes(False).shape('normal'    )
            _.add_node(label='Go shopping'  , key='B').wrap_with_quotes(False).shape('round-edge')
            _.add_node(label='Let me think' , key='C').wrap_with_quotes(False).shape('rhombus'   )
            _.add_node(label='Laptop'       , key='D').wrap_with_quotes(False)
            _.add_node(label='iPhone'       , key='E').wrap_with_quotes(False)
            _.add_node(label='fa:fa-car Car', key='F').wrap_with_quotes(False)
            _.add_edge('A', 'B', label='Get money').output_node_from().output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('B', 'C'                   ).output_node_to()
            _.add_edge('C', 'D', label='One'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'E', label='Two'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'F', label='Three'    ).output_node_to().edge_mode__lr_using_pipe()
            #_.print_code()

        assert expected_code == _.code()
        #file_path = self.mermaid.save()

    def test_config(self):
        assert self.mermaid.config__add_nodes is True

    def test__config__edge__output_node_from(self):
        with self.mermaid as _:
            new_edge = _.add_edge('id', 'id2').output_node_from()
            assert _.code()               == 'graph LR\n    id["id"]\n    id2["id2"]\n\n    id["id"] --> id2'
            assert new_edge.attributes    == {'output_node_from': True }
            assert new_edge.render_edge() == '    id["id"] --> id2'
            new_edge.output_node_from(False)
            assert new_edge.attributes    == {'output_node_from': False}
            assert new_edge.render_edge() == '    id --> id2'




    def test__config__wrap_with_quotes(self):
        new_node = Mermaid().add_node(key='id').wrap_with_quotes()
        assert new_node.attributes == {'wrap_with_quotes': True}
        assert new_node.key == 'id'
        assert new_node.data() == {'attributes' : {'wrap_with_quotes': True},
                                   'key'        : 'id'                      ,
                                   'label'      : 'id'                      }
        assert type_mro(new_node) == [Mermaid__Node, MGraph__Node, Kwargs_To_Self, object]

        with Mermaid() as _:
            _.add_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'
        with Mermaid() as _:
            _.add_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'
        with Mermaid() as _:
            _.add_node(key='id').wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = Mermaid()
        new_node = mermaid.add_node(key='id')
        new_node.wrap_with_quotes(False)
        assert type(new_node) == Mermaid__Node
        assert new_node.attributes == {'wrap_with_quotes': False}
        assert mermaid.code() == 'graph LR\n    id[id]\n'

    def test__config__node_shape(self):
        with Mermaid().add_node(key='id') as _:
            assert _                    .render_node() == '    id["id"]'
            assert _.shape(''          ).render_node() == '    id["id"]'
            assert _.shape('aaaaa'     ).render_node() == '    id["id"]'
            assert _.shape('round-edge').render_node() == '    id("id")'
            assert _.shape('rhombus'   ).render_node() == '    id{"id"}'


    #@trace_calls(contains=['mermaid'])         # this was the code that was triggering the bug
    def test_use_case_1(self):
        expected_code = """
                            flowchart LR
                               id"""

        print()
        print()

        print(str_dedent(expected_code))
        print()
        with self.mermaid as _:
            _.set_diagram_type(Diagram__Type.flowchart)
            _.add_node(key='id').wrap_with_quotes(False).shape('rhombus')
            _.print_code()
            _.save()

            assert _.code() == 'flowchart LR\n    id{id}\n'
            assert _.code() != expected_code

    def test__regression__Mermaid__Edge__is_failing_on_ctor(self):
        MGraph__Edge()                                                  # MGraph__Edge  ctor doesn't raise an exception
        mermaid_edge = Mermaid__Edge()                                  # FIXED: MGraph__Edge also now doesn't raise an exception

        assert type(mermaid_edge.from_node) is Mermaid__Node            # confirm that correct types of
        assert type(mermaid_edge.to_node  ) is Mermaid__Node            # both from_node and to_node vars

        # with self.assertRaises(Exception) as context:
        #     Mermaid__Edge()                                             # Mermaid__Edge ctor raises an exception
        # assert str(context.exception) == ("Invalid type for attribute 'from_node'. Expected '<class "
        #                                   "'osbot_utils.graphs.mermaid.Mermaid__Node.Mermaid__Node'>' but got '<class "
        #                                   "'osbot_utils.graphs.mgraph.MGraph__Node.MGraph__Node'>'")



    def test__regression__Mermaid__Edge__init__is_not_enforcing_type_safety(self):
        from_node_key = 'from_node_key'
        to_node_key   = 'to_node_key'
        from_node     = from_node_key
        to_node       = to_node_key


        assert Mermaid__Edge.__annotations__ == {'from_node': Mermaid__Node ,           # confirm the type annotations
                                                 'to_node'  : Mermaid__Node }
        assert type(from_node) is str                                                   # confirm that both variables are of type str
        assert type(to_node  ) is str
        with self.assertRaises(Exception) as context:
            Mermaid__Edge(from_node=from_node, to_node=to_node)                  # FIXED: this now raises exception: BUG, this should have not worked (an exception should have been raised)
        assert str(context.exception) == ("Invalid type for attribute 'from_node'. Expected '<class "
                                          "'osbot_utils.graphs.mermaid.Mermaid__Node.Mermaid__Node'>' but got '<class "
                                          "'str'>'")

        # assert new_edge.from_node       == from_node                                    # confirm that assigment worked
        # assert new_edge.to_node         == to_node                                      # BUG, to_node should never be anything else than a Mermaid__Node object
        # assert type(new_edge.from_node) is str                                          # confirm that the type of the variables is still str
        # assert type(new_edge.to_node  ) is str                                          # BUG, to_node should never be anything else than a Mermaid__Node object

        # with self.assertRaises(Exception) as context:
        #     new_edge.to_node = to_node                                                  # confirm that this type safety is working (i.e. assigment post ctor)
        # assert str(context.exception) == ("Invalid type for attribute 'to_node'."
        #                                   " Expected '<class 'osbot_utils.graphs."      # note how the type safety correctly picked up that we were expecting
        #                                   "mermaid.Mermaid__Node.Mermaid__Node'>' "     #     an object of type Mermaid__Node
        #                                   "but got '<class 'str'>'")                    #     but we got an object of type str







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