# Type_Safe Round-Trip Serialization: Complete Data Persistence & Network Transport Guide

## Overview

Type_Safe provides **complete round-trip serialization** - the ability to convert complex Type_Safe objects to JSON, transmit or store them, and perfectly reconstruct the original typed objects. This maintains type safety across network boundaries, file storage, and inter-process communication.

## Core Concepts

### What is Round-Trip Serialization?

Round-trip serialization ensures that:
```
Original Object → JSON → Storage/Network → JSON → Reconstructed Object
```

The reconstructed object is **identical** to the original, with:
- ✅ All type constraints preserved
- ✅ Nested objects properly typed
- ✅ Collections maintaining type safety
- ✅ Custom types (Safe_Id, etc.) restored
- ✅ Validation rules intact

## Basic Round-Trip Examples

### Simple Object Serialization

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import List, Dict, Optional

class UserProfile(Type_Safe):
    username: str
    email: str
    age: int
    tags: List[str]
    settings: Dict[str, bool]
    bio: Optional[str] = None

# Create and populate object
original = UserProfile(
    username="alice",
    email="alice@example.com",
    age=28,
    tags=["developer", "python"],
    settings={"notifications": True, "dark_mode": False}
)

# Serialize to JSON
json_data = original.json()
# Returns: {
#     "username": "alice",
#     "email": "alice@example.com", 
#     "age": 28,
#     "tags": ["developer", "python"],
#     "settings": {"notifications": true, "dark_mode": false},
#     "bio": null
# }

# Save to file
import json
with open('user.json', 'w') as f:
    json.dump(json_data, f)

# Load from file and reconstruct
with open('user.json', 'r') as f:
    loaded_data = json.load(f)

reconstructed = UserProfile.from_json(loaded_data)

# Verify perfect reconstruction
assert reconstructed.username == original.username
assert reconstructed.age == original.age
assert reconstructed.tags == original.tags
assert reconstructed.settings == original.settings
assert reconstructed.json() == original.json()  # Perfect match!
```

### Nested Objects Round-Trip

```python
class Address(Type_Safe):
    street: str
    city: str
    state: str
    zip_code: str

class Company(Type_Safe):
    name: str
    founded: int
    headquarters: Address
    branches: List[Address]
    employee_count: Dict[str, int]

# Create complex nested structure
original = Company(
    name="TechCorp",
    founded=2010,
    headquarters=Address(
        street="123 Main St",
        city="Boston",
        state="MA",
        zip_code="02101"
    ),
    branches=[
        Address(street="456 Oak Ave", city="NYC", state="NY", zip_code="10001"),
        Address(street="789 Pine Rd", city="SF", state="CA", zip_code="94102")
    ],
    employee_count={"Boston": 150, "NYC": 75, "SF": 50}
)

# Full serialization preserves structure
json_data = original.json()

# Save to file
with open('company.json', 'w') as f:
    json.dump(json_data, f, indent=2)

# Reconstruct from file
with open('company.json', 'r') as f:
    loaded = json.load(f)

reconstructed = Company.from_json(loaded)

# All nested objects are properly typed
assert isinstance(reconstructed.headquarters, Address)
assert all(isinstance(branch, Address) for branch in reconstructed.branches)
assert reconstructed.headquarters.city == "Boston"
assert len(reconstructed.branches) == 2
```

## Advanced Serialization Features

### Type-Safe Primitives Serialization

```python
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid import Random_Guid

class UserId(Safe_Id): pass
class OrderId(Safe_Id): pass

class Order(Type_Safe):
    id: OrderId
    user_id: UserId
    transaction_id: Random_Guid
    amount: float
    items: List[str]

# Create with type-safe IDs
original = Order(
    id=OrderId("ORD-12345"),
    user_id=UserId("USR-67890"),
    transaction_id=Random_Guid(),
    amount=299.99,
    items=["laptop", "mouse"]
)

# Serialize - IDs become strings
json_data = original.json()
# {
#     "id": "ORD-12345",
#     "user_id": "USR-67890",
#     "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
#     "amount": 299.99,
#     "items": ["laptop", "mouse"]
# }

# Deserialize - strings become typed IDs again!
reconstructed = Order.from_json(json_data)

# Type safety is preserved
assert isinstance(reconstructed.id, OrderId)
assert isinstance(reconstructed.user_id, UserId)
assert isinstance(reconstructed.transaction_id, Random_Guid)

# Values match
assert reconstructed.id == OrderId("ORD-12345")
assert reconstructed.user_id == UserId("USR-67890")

# Type checking still works
try:
    reconstructed.id = UserId("USR-99999")  # Wrong type!
except ValueError:
    pass  # ✓ Type safety maintained
```

### Self-Referential Structures

```python
class TreeNode(Type_Safe):
    value: int
    parent: Optional['TreeNode'] = None
    children: List['TreeNode'] = []

# Create tree structure
root = TreeNode(value=1)
child1 = TreeNode(value=2)
child2 = TreeNode(value=3)
grandchild = TreeNode(value=4)

# Build relationships
root.children = [child1, child2]
child1.children = [grandchild]

# Serialize tree
tree_json = root.json()
# {
#     "value": 1,
#     "parent": null,
#     "children": [
#         {
#             "value": 2,
#             "parent": null,
#             "children": [
#                 {"value": 4, "parent": null, "children": []}
#             ]
#         },
#         {"value": 3, "parent": null, "children": []}
#     ]
# }

# Reconstruct tree
reconstructed = TreeNode.from_json(tree_json)

# Structure is preserved
assert reconstructed.value == 1
assert len(reconstructed.children) == 2
assert reconstructed.children[0].value == 2
assert reconstructed.children[0].children[0].value == 4
```

### Type References Serialization

```python
from typing import Type, Dict

class Schema__Node(Type_Safe):
    node_type: Type['Schema__Node']
    node_id: str
    metadata: Dict[str, Any]

class Schema__Edge(Type_Safe):
    edge_type: Type['Schema__Edge']
    from_node: str
    to_node: str

class Graph(Type_Safe):
    nodes: Dict[str, Schema__Node]
    edges: List[Schema__Edge]
    graph_type: Type['Graph']

# Create with type references
graph = Graph()
graph.graph_type = Graph
graph.nodes = {
    "n1": Schema__Node(
        node_type=Schema__Node,
        node_id="n1",
        metadata={"label": "Start"}
    )
}

# Type references serialize as strings
json_data = graph.json()
# {
#     "graph_type": "Graph",
#     "nodes": {
#         "n1": {
#             "node_type": "Schema__Node",
#             "node_id": "n1",
#             "metadata": {"label": "Start"}
#         }
#     },
#     "edges": []
# }

# Reconstruct with proper types
reconstructed = Graph.from_json(json_data)
assert reconstructed.graph_type == Graph
assert reconstructed.nodes["n1"].node_type == Schema__Node
```

## Network Transport Patterns

### REST API Integration

```python
import requests
import json

class APIRequest(Type_Safe):
    method: str
    endpoint: str
    headers: Dict[str, str]
    params: Dict[str, Any]
    body: Optional[Dict[str, Any]] = None

class APIResponse(Type_Safe):
    status_code: int
    headers: Dict[str, str]
    data: Dict[str, Any]
    errors: List[str] = []

# Client side - sending request
request = APIRequest(
    method="POST",
    endpoint="/api/users",
    headers={"Content-Type": "application/json"},
    params={"validate": True},
    body={"username": "alice", "email": "alice@example.com"}
)

# Send over network
response = requests.post(
    "https://api.example.com/relay",
    json=request.json(),  # Serialize for transport
    headers={"Authorization": "Bearer token"}
)

# Server side - receiving and processing
def handle_request(json_data: dict):
    # Reconstruct typed request
    request = APIRequest.from_json(json_data)
    
    # Type-safe access to fields
    if request.method == "POST":
        process_post(request.body)
    
    # Create typed response
    response = APIResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        data={"user_id": 12345, "created": True}
    )
    
    # Send back as JSON
    return response.json()
```

### Message Queue Integration

```python
import json
from typing import Any, Dict
import pika  # RabbitMQ client

class Message(Type_Safe):
    id: str
    timestamp: float
    type: str
    payload: Dict[str, Any]
    metadata: Dict[str, str]

class MessageProcessor:
    def send_message(self, message: Message, queue: str):
        # Serialize for queue
        json_message = json.dumps(message.json())
        
        # Send to RabbitMQ
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json_message
        )
        connection.close()
    
    def receive_message(self, queue: str) -> Message:
        connection = pika.BlockingConnection()
        channel = connection.channel()
        
        method, properties, body = channel.basic_get(queue)
        if body:
            # Deserialize from queue
            json_data = json.loads(body)
            message = Message.from_json(json_data)
            
            # Type-safe message processing
            if message.type == "user_event":
                process_user_event(message.payload)
            
            return message
        
        connection.close()
```

### WebSocket Communication

```python
import asyncio
import websockets
import json

class WebSocketMessage(Type_Safe):
    action: str
    data: Dict[str, Any]
    client_id: Optional[str] = None
    timestamp: Optional[float] = None

async def client():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Send typed message
        message = WebSocketMessage(
            action="subscribe",
            data={"channel": "updates", "filters": ["important"]},
            client_id="client-123"
        )
        
        await websocket.send(json.dumps(message.json()))
        
        # Receive and deserialize response
        response_json = await websocket.recv()
        response = WebSocketMessage.from_json(json.loads(response_json))
        
        # Type-safe handling
        if response.action == "update":
            handle_update(response.data)

async def server(websocket, path):
    async for message in websocket:
        # Deserialize incoming message
        incoming = WebSocketMessage.from_json(json.loads(message))
        
        # Type-safe processing
        if incoming.action == "subscribe":
            channels = incoming.data.get("channels", [])
            # Process subscription...
            
        # Send typed response
        response = WebSocketMessage(
            action="acknowledged",
            data={"status": "success"},
            timestamp=time.time()
        )
        
        await websocket.send(json.dumps(response.json()))
```

## File Storage Patterns

### Database Storage

```python
import sqlite3
import json

class UserRecord(Type_Safe):
    id: int
    username: str
    email: str
    settings: Dict[str, Any]
    created_at: str

class UserRepository:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                data TEXT NOT NULL
            )
        ''')
    
    def save(self, user: UserRecord):
        # Serialize to JSON for storage
        json_data = json.dumps(user.json())
        
        self.conn.execute(
            "INSERT OR REPLACE INTO users (id, data) VALUES (?, ?)",
            (user.id, json_data)
        )
        self.conn.commit()
    
    def load(self, user_id: int) -> Optional[UserRecord]:
        cursor = self.conn.execute(
            "SELECT data FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        
        if row:
            # Deserialize from JSON
            json_data = json.loads(row[0])
            return UserRecord.from_json(json_data)
        return None
    
    def load_all(self) -> List[UserRecord]:
        cursor = self.conn.execute("SELECT data FROM users")
        users = []
        
        for row in cursor:
            json_data = json.loads(row[0])
            users.append(UserRecord.from_json(json_data))
        
        return users

# Usage
repo = UserRepository("users.db")

# Save user
user = UserRecord(
    id=1,
    username="alice",
    email="alice@example.com",
    settings={"theme": "dark"},
    created_at="2024-01-01T10:00:00Z"
)
repo.save(user)

# Load user
loaded_user = repo.load(1)
assert loaded_user.username == "alice"
assert isinstance(loaded_user.settings, dict)
```

### Configuration Files

```python
import json
import yaml
from pathlib import Path

class AppConfig(Type_Safe):
    app_name: str
    version: str
    debug: bool = False
    database: Dict[str, Any]
    features: List[str]
    limits: Dict[str, int]

class ConfigManager:
    def __init__(self, config_dir: Path):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def save_json(self, config: AppConfig, filename: str):
        """Save configuration as JSON"""
        filepath = self.config_dir / f"{filename}.json"
        
        with open(filepath, 'w') as f:
            json.dump(config.json(), f, indent=2)
    
    def load_json(self, filename: str) -> AppConfig:
        """Load configuration from JSON"""
        filepath = self.config_dir / f"{filename}.json"
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return AppConfig.from_json(data)
    
    def save_yaml(self, config: AppConfig, filename: str):
        """Save configuration as YAML"""
        filepath = self.config_dir / f"{filename}.yaml"
        
        with open(filepath, 'w') as f:
            yaml.dump(config.json(), f, default_flow_style=False)
    
    def load_yaml(self, filename: str) -> AppConfig:
        """Load configuration from YAML"""
        filepath = self.config_dir / f"{filename}.yaml"
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        return AppConfig.from_json(data)

# Usage
config = AppConfig(
    app_name="MyApp",
    version="1.0.0",
    debug=True,
    database={
        "host": "localhost",
        "port": 5432,
        "name": "myapp_db"
    },
    features=["auth", "api", "websocket"],
    limits={"max_connections": 100, "timeout": 30}
)

manager = ConfigManager("./configs")

# Save in different formats
manager.save_json(config, "app_config")
manager.save_yaml(config, "app_config")

# Load and verify
loaded_json = manager.load_json("app_config")
loaded_yaml = manager.load_yaml("app_config")

assert loaded_json.json() == config.json()
assert loaded_yaml.json() == config.json()
```

## Compression and Optimization

### Compressed Serialization

```python
import json
import gzip
import base64

class DataPacket(Type_Safe):
    id: str
    timestamp: float
    sensor_data: List[float]
    metadata: Dict[str, Any]

class CompressedSerializer:
    @staticmethod
    def compress(obj: Type_Safe) -> str:
        """Compress Type_Safe object to base64 string"""
        # Convert to JSON
        json_str = json.dumps(obj.json())
        
        # Compress with gzip
        compressed = gzip.compress(json_str.encode('utf-8'))
        
        # Encode as base64 for transport
        return base64.b64encode(compressed).decode('ascii')
    
    @staticmethod
    def decompress(data: str, cls: Type[Type_Safe]) -> Type_Safe:
        """Decompress base64 string to Type_Safe object"""
        # Decode from base64
        compressed = base64.b64decode(data.encode('ascii'))
        
        # Decompress
        json_str = gzip.decompress(compressed).decode('utf-8')
        
        # Parse JSON and create object
        json_data = json.loads(json_str)
        return cls.from_json(json_data)

# Create large data packet
packet = DataPacket(
    id="sensor-001",
    timestamp=1234567890.123,
    sensor_data=[float(i) * 0.1 for i in range(1000)],
    metadata={"location": "Lab A", "experiment": "Test 42"}
)

# Compress for storage/transport
compressed = CompressedSerializer.compress(packet)
print(f"Compressed size: {len(compressed)} bytes")

# Decompress and reconstruct
reconstructed = CompressedSerializer.decompress(compressed, DataPacket)

# Verify integrity
assert reconstructed.id == packet.id
assert len(reconstructed.sensor_data) == 1000
assert reconstructed.sensor_data[500] == packet.sensor_data[500]
```

### Optimized JSON Compression

Type_Safe includes built-in JSON compression for efficient serialization:

```python
# Using built-in compression
class LargeDataset(Type_Safe):
    records: List[Dict[str, Any]]
    metadata: Dict[str, str]

dataset = LargeDataset(
    records=[{"id": i, "value": f"data_{i}"} for i in range(100)],
    metadata={"source": "sensor", "version": "2.0"}
)

# Compress using Type_Safe's built-in compression
compressed_json = dataset.json__compress()

# Decompress
reconstructed = LargeDataset.from_json__compressed(compressed_json)

assert len(reconstructed.records) == 100
```

## Error Handling and Validation

### Robust Deserialization

```python
class SafeDeserializer:
    @staticmethod
    def from_json_safe(
        cls: Type[Type_Safe],
        data: Any,
        strict: bool = False
    ) -> Optional[Type_Safe]:
        """Safely deserialize with error handling"""
        
        try:
            # Handle different input types
            if isinstance(data, str):
                json_data = json.loads(data)
            elif isinstance(data, bytes):
                json_data = json.loads(data.decode('utf-8'))
            elif isinstance(data, dict):
                json_data = data
            else:
                raise ValueError(f"Unsupported data type: {type(data)}")
            
            # Attempt deserialization
            return cls.from_json(json_data, raise_on_not_found=strict)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
        except ValueError as e:
            print(f"Validation error: {e}")
            if strict:
                raise
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

# Usage with error handling
json_string = '{"username": "alice", "age": "not_a_number"}'

# Non-strict mode - returns None on error
user = SafeDeserializer.from_json_safe(UserProfile, json_string, strict=False)
if user is None:
    print("Failed to deserialize user")

# Strict mode - raises exception
try:
    user = SafeDeserializer.from_json_safe(UserProfile, json_string, strict=True)
except ValueError as e:
    print(f"Strict validation failed: {e}")
```

## Best Practices

### 1. Version Your Schemas

```python
class VersionedSchema(Type_Safe):
    version: int = 1
    data: Dict[str, Any]

    @classmethod
    def migrate(cls, json_data: dict) -> dict:
        """Migrate old versions to current"""
        version = json_data.get('version', 1)
        
        if version == 1 and cls.version == 2:
            # Migrate from v1 to v2
            json_data['version'] = 2
            json_data['new_field'] = 'default_value'
        
        return json_data
    
    @classmethod
    def from_json(cls, json_data: dict):
        # Migrate if needed
        json_data = cls.migrate(json_data)
        return super().from_json(json_data)
```

### 2. Handle Partial Data

```python
class RobustModel(Type_Safe):
    required_field: str
    optional_field: Optional[str] = None
    with_default: int = 100
    
    @classmethod
    def from_partial(cls, partial_data: dict):
        """Create from partial data with defaults"""
        # Start with defaults
        full_data = {
            'required_field': partial_data.get('required_field', ''),
            'optional_field': partial_data.get('optional_field'),
            'with_default': partial_data.get('with_default', 100)
        }
        
        return cls.from_json(full_data)
```

### 3. Validate Before Serialization

```python
class ValidatedModel(Type_Safe):
    email: str
    age: int
    
    def validate(self) -> List[str]:
        """Validate before serialization"""
        errors = []
        
        if '@' not in self.email:
            errors.append("Invalid email format")
        if not 0 <= self.age <= 150:
            errors.append("Age out of valid range")
        
        return errors
    
    def json_validated(self) -> Optional[dict]:
        """Only serialize if valid"""
        errors = self.validate()
        if errors:
            raise ValueError(f"Validation failed: {errors}")
        return self.json()
```

## Summary

Type_Safe's round-trip serialization provides:

- ✅ **Perfect Fidelity** - Objects reconstruct exactly as they were
- ✅ **Type Safety** - All type constraints preserved through serialization
- ✅ **Network Ready** - JSON format works with any transport
- ✅ **Storage Flexible** - Save to files, databases, caches
- ✅ **Compression Support** - Built-in and custom compression options
- ✅ **Error Resilient** - Robust deserialization with validation

This makes Type_Safe ideal for:
- Distributed systems
- Microservices communication  
- Configuration management
- Data persistence
- Message queuing
- API development
- State synchronization

The round-trip capability ensures your type safety extends beyond process boundaries, maintaining data integrity across your entire system architecture.