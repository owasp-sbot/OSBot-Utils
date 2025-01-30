# OSBot-Utils Flow System Documentation

## Overview

The Flow system in OSBot-Utils is designed to solve the common challenge of orchestrating complex task execution in Python applications. Unlike simple sequential execution, the Flow system provides a rich context that enables monitoring, debugging, and maintenance of task execution flows. This is particularly valuable in applications that require robust error handling, detailed logging, and complex task dependencies.

## Core Components

### Flow

The Flow class serves as the execution context and lifecycle manager for tasks. Think of it as a container that provides the environment and services needed by tasks. When a Flow executes, it maintains state information, manages resources, and coordinates the execution of tasks. The Flow instance becomes a central point for monitoring progress, handling errors, and collecting results.

Key aspects of Flow:
- **Task execution monitoring**: Tracks the progress and status of each task
- **Event emission**: Notifies listeners about important lifecycle events
- **Structured logging**: Maintains organized, contextual logs
- **Error handling**: Manages and propagates errors appropriately
- **Data sharing**: Provides mechanisms for tasks to share data
- **Artifact management**: Stores and manages execution artifacts

### Task 

Tasks represent individual units of work within a Flow. They are designed to be self-contained, reusable components that can access the services provided by their parent Flow. Tasks can be created either through decoration or direct instantiation, offering flexibility in how you structure your code.

Key aspects of Task:
- **Flow context discovery**: Automatically finds its parent Flow
- **Dependency injection**: Receives required dependencies automatically
- **Error handling**: Configurable error behavior
- **Event emission**: Notifies about task lifecycle events
- **Data access**: Can access shared Flow data

### Event System

The event system provides real-time visibility into Flow and Task execution. It uses an observer pattern where listeners can subscribe to various types of events. This is particularly useful for monitoring, debugging, and integrating with external systems.

Event types and their purposes:
```python
Flow_Run__Event_Type:
- FLOW_START   : Marks the beginning of flow execution
   Used to initialize resources and prepare for execution
   
- FLOW_STOP    : Marks the completion of flow execution
   Used for cleanup and final status reporting
   
- TASK_START   : Indicates a task is beginning
   Useful for tracking task progress and timing
   
- TASK_STOP    : Indicates a task has completed
   Captures task results and execution metrics
   
- FLOW_MESSAGE : Carries log messages
   Provides detailed execution information
   
- NEW_ARTIFACT : Indicates new artifact creation
   Tracks data products and intermediary results
   
- NEW_RESULT   : Indicates result generation
   Captures final or important intermediate results
```

## Configuration

### Flow Configuration (Flow_Run__Config)

The configuration system provides fine-grained control over Flow behavior. Each setting affects a specific aspect of Flow execution, allowing you to customize the behavior for different use cases.

```python
class Flow_Run__Config:
    # Controls whether tasks are added to the flow instance
    # Useful for tracking task history and relationships
    add_task_to_self         : bool = True    
    
    # Determines if logs should be written to console
    # Helpful for development and debugging
    log_to_console           : bool = False   
    
    # Controls in-memory log retention
    # Important for post-execution analysis
    log_to_memory           : bool = True    
    
    # Master switch for logging functionality
    # Can disable all logging for performance
    logging_enabled         : bool = True    
    
    # Controls automatic log printing after execution
    # Useful for immediate feedback
    print_logs             : bool = False   
    
    # Determines if None returns are printed
    # Helps track task completion
    print_none_return_value: bool = False   
    
    # Controls end-of-execution messages
    # Provides execution boundaries
    print_finished_message : bool = False   
    
    # Controls error propagation
    # Critical for error handling strategy
    raise_flow_error       : bool = True    
```

Each configuration option serves a specific purpose:

**add_task_to_self (True)**:
- Maintains a list of executed tasks in the Flow instance
- Enables task history tracking and debugging
- Useful for understanding task execution patterns

**log_to_console (False)**:
- Controls immediate visibility of log messages
- Helpful during development and debugging
- Can be disabled in production for performance

**log_to_memory (True)**:
- Keeps logs in memory for later analysis
- Enables post-execution log examination
- Important for debugging and audit trails

**logging_enabled (True)**:
- Master switch for all logging features
- Can be disabled for maximum performance
- Affects both console and memory logging

**print_logs (False)**:
- Automatically prints logs after Flow completion
- Provides immediate execution feedback
- Useful for interactive development

**print_none_return_value (False)**:
- Controls visibility of None returns
- Helps track task completion
- Useful for debugging task chains

**print_finished_message (False)**:
- Marks Flow completion in logs
- Helps track Flow boundaries
- Useful in multi-Flow scenarios

**raise_flow_error (True)**:
- Controls error propagation strategy
- Affects Flow error handling behavior
- Critical for application error management

## Usage Patterns

### Basic Flow Usage

The basic usage pattern demonstrates how to create and execute simple Flows. This pattern is the foundation for more complex implementations.

```python
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.helpers.flows.decorators.task import task

# Define a flow that processes input data
@flow()
def my_flow(input_data):
    # The flow coordinates the overall process
    result = process_data(input_data)
    return result

# Define a task that performs specific work
@task()
def process_data(data):
    # Tasks handle individual units of work
    # This could be data transformation, API calls, etc.
    return processed_data

# Execute the flow and get results
flow_instance = my_flow(data).execute()
```

This pattern shows several key concepts:
1. Flow definition using decorators
2. Task integration within flows
3. Data passing between components
4. Flow execution and result handling

### Task Dependencies and Data Sharing

The dependency injection system automates the provision of common dependencies to tasks. This reduces boilerplate code and makes tasks more modular.

```python
@task()
def task_with_deps(this_task=None, this_flow=None, task_data=None, flow_data=None):
    # this_task: Access to task instance for internal operations
    # this_flow: Access to parent flow for flow-level operations
    # task_data: Task-specific storage that doesn't persist
    # flow_data: Flow-wide storage shared between tasks
    
    # Task-specific data example
    task_data['local'] = 'only visible to this task'
    
    # Flow-wide data example
    flow_data['shared'] = 'visible to all tasks'
```

Key aspects of dependency injection:
1. Automatic dependency resolution
2. Scoped data storage
3. Access to flow and task contexts
4. Clean separation of concerns

### Async Support

The Flow system fully supports asynchronous execution, allowing efficient handling of I/O-bound operations.

```python
@flow()
async def async_flow():
    # Flows can be async
    result = await async_task()
    return result

@task()
async def async_task():
    # Tasks can be async
    await asyncio.sleep(1)
    return "completed"
```

Async support features:
1. Compatible with asyncio
2. Maintains Flow context in async operations
3. Supports mixed sync/async tasks
4. Preserves error handling and logging

### Error Handling

The error handling system provides flexible control over how errors are managed at both Flow and Task levels.

```python
# Task-level error handling
@task(raise_on_error=False)
def task_continues_on_error():
    # This error won't stop the flow
    raise ValueError("Task error")

# Flow-level error handling
flow_config = Flow_Run__Config(raise_flow_error=False)
@flow(flow_config=flow_config)
def flow_continues_on_error():
    # Flow continues despite task errors
    task_continues_on_error()
    return "Flow completed despite error"
```

Error handling features:
1. Configurable error propagation
2. Detailed error logging
3. Error context preservation
4. Flexible recovery options

### Event Listening

The event system enables real-time monitoring and reaction to Flow and Task execution events.

```python
def event_listener(event: Flow_Run__Event):
    # Handle different event types
    if event.event_type == Flow_Run__Event_Type.TASK_START:
        print(f"Task started: {event.event_data.task_name}")
    elif event.event_type == Flow_Run__Event_Type.FLOW_MESSAGE:
        print(f"Log message: {event.event_data.data['message_data']['message']}")

# Register the listener
flow_events.event_listeners.append(event_listener)
```

Event system features:
1. Real-time event notification
2. Structured event data
3. Multiple listener support
4. Error-resistant event dispatch

### Artifacts and Results

The artifact system provides a structured way to store and track data products and results.

```python
@flow()
def flow_with_artifacts(this_flow=None):
    # Store structured data as an artifact
    this_flow.add_flow_artifact(
        description="API Response",
        key="api-response",
        data={"status": "success"},
        artifact_type="json"
    )
    
    # Record a result
    this_flow.add_flow_result(
        key="calculation-result",
        description="Final calculation value: 42"
    )
```

Artifact system features:
1. Structured data storage
2. Result tracking
3. Artifact type classification
4. Event notification

## Technical Details

### Flow Lifecycle

The Flow lifecycle consists of several distinct phases, each with specific responsibilities:

1. Flow Creation
   - Instance initialization
   - Configuration application
   - Event listener setup
   - Resource preparation

2. Flow Execution
   - Event notification
   - Argument resolution
   - Task coordination
   - Result collection
   - Resource cleanup

3. Task Execution
   - Context discovery
   - Event notification
   - Dependency injection
   - Output capture
   - Error handling

### Context Discovery

The context discovery system uses stack inspection to locate the parent Flow:

```python
def find_flow(self):
    # Examine the call stack
    stack = inspect.stack()
    for frame_info in stack:
        frame = frame_info.frame
        # Look for Flow instances
        for var_name, var_value in frame.f_locals.items():
            if type(var_value) is Flow:
                return var_value
    return None
```

Context discovery features:
1. Automatic Flow location
2. Stack frame examination
3. Variable inspection
4. Robust error handling

### Dependency Injection

The dependency injection system automatically provides required dependencies:

Key features:
1. Automatic dependency resolution
2. Type-based injection
3. Named parameter matching
4. Default value support

### Event Data Structure

Events carry structured data about Flow and Task execution:

```python
class Flow_Run__Event_Data:
    data        : dict   # Event-specific payload
    event_source: str    # Event origin
    flow_name   : str    # Flow identifier
    flow_run_id : str    # Execution identifier
    log_level   : int    # Message severity
    task_name   : str    # Task identifier
    task_run_id : str    # Task execution identifier
```

Event data features:
1. Structured information
2. Context preservation
3. Unique identification
4. Severity classification

## Best Practices

### 1. Flow Organization
Organize flows to maximize reusability and maintainability:
- Group related tasks
- Use meaningful names
- Maintain single responsibility
- Document flow purpose

### 2. Error Handling
Implement robust error handling strategies:
- Configure appropriate levels
- Use task-level controls
- Add detailed logging
- Plan recovery paths

### 3. Data Management
Manage data effectively:
- Use appropriate scopes
- Clean up when done
- Document data structures
- Handle sensitive data

### 4. Event Handling
Implement efficient event handling:
- Keep listeners light
- Manage listener lifecycle
- Handle errors gracefully
- Document event usage

### 5. Async Usage
Use async features effectively:
- Separate I/O operations
- Maintain clean async boundaries
- Handle contexts properly
- Monitor performance

## Common Patterns and Examples

### Data Processing Pipeline

Example of a data processing pipeline:
- Shows task sequencing
- Demonstrates data validation
- Illustrates error handling
- Shows data sharing

### API Integration

Example of API integration:
- Shows async usage
- Demonstrates error handling
- Illustrates artifact storage
- Shows logging patterns

## Advanced Features

### Custom Event Handlers
Create specialized event handlers:
- Track metrics
- Monitor performance
- Log to external systems
- Trigger actions

### Flow Extensions

Extend Flow functionality:
- Add custom features
- Enhance logging
- Add metrics
- Customize behavior

## Debugging and Troubleshooting

### Common Issues

Solutions for common problems:
1. Flow context issues
2. Event listener problems
3. Dependency injection failures
4. Error handling challenges

### Debugging Tools

Tools and techniques for debugging:
1. Enhanced logging
2. Event debugging
3. Task tracing
4. Performance monitoring

## Performance Considerations

Optimize Flow system performance:
1. Event listener efficiency
2. Memory management
3. Async optimization
4. Resource cleanup

## Security Considerations

Implement secure Flow usage:
1. Data handling
2. Error message security
3. Artifact protection
4. Access control

## Testing

Implement comprehensive testing:
1. Unit testing
2. Integration testing
3. Event testing
4. Performance testing

## Contributing

Guidelines for contributors:
1. Feature additions
2. Bug fixes
3. Documentation
4. Testing requirements

## Version History

Track system evolution:
- Initial release
- Feature additions
- Bug fixes
- Improvements

## Future Considerations

Plan for future development:
1. Planned features
2. Improvements
3. Research areas
4. Performance enhancements

Would you like me to expand on any particular aspect further or add more specific examples?