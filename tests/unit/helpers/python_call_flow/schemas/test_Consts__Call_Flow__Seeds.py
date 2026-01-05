from osbot_utils.helpers.python_call_flow.schemas.Consts__Call_Flow__Seeds import SEED__ONTOLOGY, SEED__NODE_TYPE__CLASS, SEED__NODE_TYPE__METHOD, SEED__PREDICATE__CALLS, SEED__NODE_TYPE__FUNCTION, \
    SEED__NODE_TYPE__MODULE, SEED__PREDICATE__CALLS_SELF, SEED__PREDICATE__CONTAINS, SEED__PREDICATE__CALLS_CHAIN, SEED__NODE_TYPE__EXTERNAL


class test_Consts__Call_Flow__Seeds:

    def test_seed_constants_exist(self):

        assert SEED__ONTOLOGY == 'call_flow:ontology'
        assert 'class'  in SEED__NODE_TYPE__CLASS
        assert 'method' in SEED__NODE_TYPE__METHOD
        assert 'calls'  in SEED__PREDICATE__CALLS

    def test_all_seeds_unique(self):
        seeds = [SEED__ONTOLOGY, SEED__NODE_TYPE__CLASS, SEED__NODE_TYPE__METHOD,
                 SEED__NODE_TYPE__FUNCTION, SEED__NODE_TYPE__MODULE, SEED__NODE_TYPE__EXTERNAL,
                 SEED__PREDICATE__CONTAINS, SEED__PREDICATE__CALLS,
                 SEED__PREDICATE__CALLS_SELF, SEED__PREDICATE__CALLS_CHAIN]
        assert len(seeds) == len(set(seeds)), "Seeds must be unique"

