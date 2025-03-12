from typing                                                         import Dict, Optional, List, Set
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.helpers.Timestamp_Now                              import Timestamp_Now
from osbot_utils.helpers.llms.schemas.Schema__LLM_Cache__Index      import Schema__LLM_Cache__Index
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request           import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response          import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache   import Schema__LLM_Response__Cache
from osbot_utils.helpers.safe_str.Safe_Str__Hash                    import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from osbot_utils.utils.Json                                         import json_to_str, json_md5
from osbot_utils.utils.Misc                                         import str_md5

SIZE__VALUE_HASH = 10

class LLM_Request__Cache(Type_Safe):
    cache_index      : Schema__LLM_Cache__Index                                             # Index mapping request hashes to cache entries
    cache_entries    : Dict[Obj_Id, Schema__LLM_Response__Cache]                            # In-memory storage of cache entries

    def save(self) -> bool:                                                                 # For overriding in subclasses
        return True

    @type_safe
    def compute_request_hash(self, request: Schema__LLM_Request) -> Safe_Str__Hash:         # Computes hash for full request
        request_json = request.request_data.json()
        hash_value   = json_md5(request_json)[:SIZE__VALUE_HASH]
        return Safe_Str__Hash(hash_value)

    @type_safe
    def compute_messages_hash(self, request: Schema__LLM_Request) -> str:                   # Computes hash for messages only
        messages_json = request.request_data.messages.json()                                # uses Type_Safe_List.json() here
        hash_value    = json_md5(messages_json)[:SIZE__VALUE_HASH]
        return Safe_Str__Hash(hash_value)

    @type_safe
    def add(self, request     : Schema__LLM_Request ,                                       # Request to cache
                  response    : Schema__LLM_Response                                        # Response to store
             ) -> Obj_Id:                                                                   # returns cache_id

        hash_request          = self.compute_request_hash (request)                         # calculate request hash
        hash_request_messages = self.compute_messages_hash(request)                         # calculate messages_hash hash
        cache_entry           = Schema__LLM_Response__Cache(cache_id                = Obj_Id()             ,              # Create a cache entry
                                                            llm_request             = request              ,
                                                            llm_response            = response             ,
                                                            hash__request           = hash_request         ,
                                                            hash__request__messages = hash_request_messages)
        cache_id             = cache_entry.cache_id


        if hash_request_messages not in self.cache_index.cache_ids__from__hash__request__messages:
            self.cache_index.cache_ids__from__hash__request__messages[hash_request_messages] = set()

        self.cache_index.cache_id__from__hash__request          [hash_request] = cache_id                                      # Update the cache index
        self.cache_entries                      [cache_id             ] = cache_entry                                   # Store in memory
        self.cache_index.cache_ids__from__hash__request__messages[hash_request_messages].add(cache_id)

        return cache_id

    def get(self, request: Schema__LLM_Request) -> Optional[Schema__LLM_Response]:                                      # Cached response or None
        request_hash = self.compute_request_hash(request)

        if request_hash in self.cache_index.cache_id__from__hash__request:                                                              # Check if we have an exact match
            cache_id    = self.cache_index.cache_id__from__hash__request[request_hash]
            cache_entry = self.get_cache_entry(cache_id)
            if cache_entry:
                return cache_entry.llm_response

        return None

    @type_safe
    def get_cache_entry(self, cache_id: Obj_Id) -> Optional[Schema__LLM_Response__Cache]:                               # Get cache entry by ID
        return self.cache_entries.get(cache_id)

    def get__same_messages(self, request: Schema__LLM_Request) -> List[Schema__LLM_Response]:                           # List of similar responses
        results       = []
        messages_hash = self.compute_messages_hash(request)

        if messages_hash in self.cache_index.cache_ids__from__hash__request__messages:
            cache_ids = self.cache_index.cache_ids__from__hash__request__messages[messages_hash]
            for cache_id in cache_ids:
                cache_entry = self.get_cache_entry(cache_id)
                if cache_entry:
                    results.append(cache_entry.llm_response)

        return results

    def exists(self, request: Schema__LLM_Request) -> bool:                                                             # True if in cache
        request_hash = self.compute_request_hash(request)
        return request_hash in self.cache_index.cache_id__from__hash__request

    def delete(self, request : Schema__LLM_Request) -> bool:                                                            # Success status
        request_hash  = self.compute_request_hash(request)
        messages_hash = self.compute_messages_hash(request)

        if request_hash not in self.cache_index.cache_id__from__hash__request:
            return False

        cache_id = self.cache_index.cache_id__from__hash__request[request_hash]

        del self.cache_index.cache_id__from__hash__request[request_hash]                                                                # Remove from hashes

        if messages_hash in self.cache_index.cache_ids__from__hash__request__messages:
            if cache_id in self.cache_index.cache_ids__from__hash__request__messages[messages_hash]:
                self.cache_index.cache_ids__from__hash__request__messages[messages_hash].remove(cache_id)

            if not self.cache_index.cache_ids__from__hash__request__messages[messages_hash]:
                del self.cache_index.cache_ids__from__hash__request__messages[messages_hash]

        if cache_id in self.cache_entries:                                                                              # Remove from memory
            del self.cache_entries[cache_id]

        return self.save()

    def get_by_id(self, cache_id : Obj_Id)-> Optional[Schema__LLM_Response]:                                            # Cached response or None
        cache_entry = self.get_cache_entry(cache_id)
        if cache_entry:
            return cache_entry.llm_response
        return None

    def clear(self) -> bool:                                                                                            # Clear all cache entries
        self.cache_index    = Schema__LLM_Cache__Index()
        self.cache_entries  = {}
        return self.save()

    def stats(self) -> Dict:                                                                                            # Cache statistics

        total_entries    = len(self.cache_index.cache_id__from__hash__request)
        models           = {}
        oldest_timestamp = None
        newest_timestamp = None

        for cache_id, entry in self.cache_entries.items():                                                          # Track models
            model = entry.llm_request.request_data.model
            if model in models:
                models[model] += 1
            else:
                models[model] = 1

            timestamp = entry.llm_response.timestamp                                                                # Track timestamps
            if oldest_timestamp is None or timestamp < oldest_timestamp:
                oldest_timestamp = timestamp
            if newest_timestamp is None or timestamp > newest_timestamp:
                newest_timestamp = timestamp

        return { "total_entries" : total_entries                                       ,
                 "models"        : models                                              ,
                 "oldest_entry"  : str(oldest_timestamp) if oldest_timestamp else None ,
                 "newest_entry"  : str(newest_timestamp) if newest_timestamp else None }