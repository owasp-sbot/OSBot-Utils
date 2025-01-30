# OSBot-Utils Flow System Documentation

## Overview

The Flow system is part of the OSBot-Utils package (available at https://github.com/owasp-sbot/OSBot-Utils) and was inspired by the excellent open-source project 'Prefect' (Pythonic orchestration for modern teams). Building on Prefect's foundations, the Flow system in OSBot-Utils is designed to solve the common challenge of orchestrating complex task execution in Python applications, with a strong focus on making the API as Pythonic and intuitive as possible.

Unlike simple sequential execution, the Flow system provides a rich context that enables monitoring, debugging, and maintenance of task execution flows. This is particularly valuable in applications that require robust error handling, detailed logging, and complex task dependencies.

### Quick Start Examples

The Flow system is designed to be incredibly intuitive and Pythonic. Here are some simple examples to get you started:

```python
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.helpers.flows.decorators.task import task

# Simple example: A flow with a single task
@flow()
def simple_flow(data):
    result = process_data(data)
    return result

@task()
def process_data(data):
    return data.upper()

# Use it naturally like any Python function
result = simple_flow("hello world").execute()
```

Context manager style for more complex flows:
```python
with ComplexDataFlow() as flow:
    flow.input_data = my_data
    result = flow.execute()
    print(f"Processing complete: {result}")
```

### Prefect Compatibility

The Flow system is 100% compatible with Prefect, allowing you to easily integrate with existing Prefect workflows. Here's a real-world example showing how the Flow system can be used in a web service context:

```python
def url_pdf(self, url="https://httpbin.org/get", return_file:bool=False):
    self.install_browser()
    with Flow__Playwright__Get_Page_Pdf() as _:
        _.url = url
        run_data   = _.run()
        pdf_bytes  = run_data.get('pdf_bytes')
        pdf_base64 = run_data.get('pdf_base64')

        if return_file is True:
            pdf_stream = io.BytesIO(pdf_bytes)
            response = StreamingResponse(
                pdf_stream,
                media_type = "application/pdf",
                headers    = {"Content-Disposition": "attachment; filename=document.pdf"}
            )
        else:
            response = {'pdf_base64': pdf_base64}

        return response
```

This example demonstrates how the Flow system can be used to:
- Handle complex browser automation tasks
- Manage resource lifecycles
- Process and transform data
- Integrate with web services
- Maintain compatibility with Prefect workflows

## Common Patterns and Examples

### Data Processing Pipeline

Here's an expanded example of a data processing pipeline that demonstrates key Flow system capabilities:

```python
class DataProcessingFlow(Type_Safe):
    @task()
    async def fetch_data(self, flow_data: dict):
        # Simulating data fetch
        raw_data = await self.data_source.fetch()
        flow_data['raw_data'] = raw_data
        
    @task()
    def validate_data(self, flow_data: dict):
        raw_data = flow_data['raw_data']
        if not self.validator.is_valid(raw_data):
            raise ValueError("Invalid data format")
            
    @task()
    def transform_data(self, flow_data: dict):
        raw_data = flow_data['raw_data']
        transformed = self.transformer.process(raw_data)
        flow_data['transformed_data'] = transformed
        
    @task()
    async def store_results(self, flow_data: dict):
        transformed = flow_data['transformed_data']
        await self.storage.save(transformed)
        
    @flow()
    async def process_data(self) -> Flow:
        await self.fetch_data()
        self.validate_data()
        self.transform_data()
        await self.store_results()
        return 'processing complete'
```

This example shows:
- Task sequencing
- Data validation
- Error handling
- Data sharing between tasks
- Mixed sync/async operations

### Web Automation Example

Building on our previous Playwright examples, here's a complete web automation flow that demonstrates real-world usage:

```python
class Flow__Web__Automation(Type_Safe):
    playwright_serverless : Playwright__Serverless
    url                   : str = 'https://example.com'
    
    @task()
    async def setup_browser(self) -> Browser:
        await self.playwright_serverless.launch()
        await self.playwright_serverless.new_page()
        print('Browser setup complete')
        
    @task()
    async def navigate_and_wait(self) -> None:
        await self.playwright_serverless.goto(self.url)
        await asyncio.sleep(1)  # Allow page to stabilize
        
    @task()
    async def perform_interactions(self, flow_data: dict) -> None:
        page = self.playwright_serverless.page
        await page.click('#main-button')
        content = await page.content()
        flow_data['page_content'] = content
        
    @task()
    def process_results(self, flow_data: dict) -> None:
        content = flow_data['page_content']
        results = self.analyze_content(content)
        flow_data['analysis_results'] = results
        
    @flow()
    async def execute_automation(self) -> Flow:
        await self.setup_browser()
        await self.navigate_and_wait()
        await self.perform_interactions()
        self.process_results()
        return 'automation complete'
```

This example demonstrates:
- Browser automation
- Resource management
- Error handling
- Data capture and processing
- Flow orchestration

## Implementation Guidelines

### Error Recovery Strategies

1. **Task-Level Recovery**
```python
@task(raise_on_error=False)
async def resilient_task(this_flow=None):
    try:
        await perform_operation()
    except Exception as error:
        this_flow.add_flow_artifact(
            key="error_details",
            data=str(error),
            artifact_type="error"
        )
        return "fallback_value"
```

2. **Flow-Level Recovery**
```python
@flow()
async def resilient_flow():
    try:
        await main_task()
    except Exception:
        await cleanup_task()
        await fallback_task()
```

### Resource Management

1. **Context Manager Pattern**
```python
class ManagedResourceFlow(Type_Safe):
    def __enter__(self):
        # Setup resources
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup resources
        pass
```

2. **Async Resource Management**
```python
class AsyncResourceFlow(Type_Safe):
    async def __aenter__(self):
        await self.setup_resources()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup_resources()
```

### Performance Optimization

1. **Minimal Logging**
```python
flow_config = Flow_Run__Config(
    log_to_memory=False,
    log_to_console=False
)
```

2. **Efficient Task Design**
```python
@task()
def optimized_task(flow_data: dict):
    # Process only required data
    subset = {k: flow_data[k] for k in required_keys}
    result = process_subset(subset)
    # Store only necessary results
    flow_data.update(result)
```

### Testing Strategies

1. **Mock Dependencies**
```python
@task()
def testable_task(this_flow=None):
    # Dependencies can be mocked for testing
    service = this_flow.get_service()
    return service.operation()
```

2. **Flow Testing**
```python
def test_flow():
    with MockedDependencies():
        flow = TestFlow()
        result = flow.execute()
        assert result.status == 'success'
```

## Advanced Topics

### Custom Event Handlers

```python
class CustomEventHandler:
    def __init__(self):
        self.events = []
        
    def handle_event(self, event: Flow_Run__Event):
        if event.event_type == Flow_Run__Event_Type.TASK_START:
            self.handle_task_start(event)
        elif event.event_type == Flow_Run__Event_Type.TASK_STOP:
            self.handle_task_stop(event)
            
    def handle_task_start(self, event):
        task_name = event.event_data.task_name
        self.events.append(f"Started: {task_name}")
        
    def handle_task_stop(self, event):
        task_name = event.event_data.task_name
        self.events.append(f"Completed: {task_name}")
```

### Custom Flow Configurations

```python
class CustomFlowConfig(Flow_Run__Config):
    def __init__(self):
        super().__init__()
        self.log_to_console = True
        self.print_logs = True
        
    def custom_setup(self):
        # Additional setup logic
        pass
```

### Integration Patterns

1. **External Service Integration**
```python
class ServiceIntegrationFlow(Type_Safe):
    @task()
    async def call_service(self, flow_data: dict):
        response = await self.service.call()
        flow_data['service_response'] = response
        
    @task()
    def process_response(self, flow_data: dict):
        response = flow_data['service_response']
        result = self.process(response)
        return result
```

2. **Database Integration**
```python
class DatabaseFlow(Type_Safe):
    @task()
    async def fetch_records(self, flow_data: dict):
        async with self.db.session() as session:
            records = await session.query(Model).all()
            flow_data['records'] = records
            
    @task()
    def process_records(self, flow_data: dict):
        records = flow_data['records']
        return [self.transform(record) for record in records]
```

## Conclusion

The Flow system provides a robust foundation for building complex, maintainable Python applications. By following these patterns and guidelines, developers can create reliable, testable, and efficient solutions for a wide range of use cases. Flow

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

The Flow system fully supports asynchronous execution, allowing efficient handling of I/O-bound operations. This is particularly valuable for web automation and network operations.

```python
@flow()
async def async_flow():
    result = await async_task()
    return result

@task()
async def async_task():
    await asyncio.sleep(1)
    return "completed"
```

A real-world example from web automation shows how async flows handle complex operations:

```python
class WebAutomationFlow(Type_Safe):
    @task()
    async def launch_browser(self) -> Browser:
        await self.browser_instance.launch()
        print('launched browser')

    @task()
    async def navigate(self) -> None:
        print(f"opening url: {self.target_url}")
        await self.browser_instance.goto(self.target_url)
        await asyncio.sleep(1)  # Ensure page load

    @flow()
    async def execute_automation(self) -> Flow:
        await self.launch_browser()
        await self.navigate()
        return 'completed'
```

Async support features:
1. Compatible with asyncio
2. Maintains Flow context in async operations
3. Supports mixed sync/async tasks
4. Preserves error handling and logging
5. Handles browser automation gracefully
6. Supports wait operations and timing controls

### Real-World Implementation Patterns

#### Web Automation Pattern

The Flow system excels at managing complex web automation tasks, as demonstrated by the Playwright integration examples:

```python
class Flow__Playwright__Operation(Type_Safe):
    playwright_serverless : Playwright__Serverless
    url                   : str = 'https://example.com'

    @task()
    def check_config(self) -> Browser:
        print('checking config')

    @task()
    async def launch_browser(self) -> Browser:
        await self.playwright_serverless.launch()

    @task()
    async def new_page(self) -> Browser:
        await self.playwright_serverless.new_page()

    @task()
    async def perform_operation(self, flow_data: dict) -> None:
        # Operation-specific logic here
        pass

    @flow()
    async def execute(self) -> Flow:
        self.check_config()
        await self.launch_browser()
        await self.new_page()
        await self.perform_operation()
        return 'all done'
```

This pattern showcases several important concepts:
1. **Resource Management**: Browser lifecycle handling
2. **Flow Data**: Using flow_data for sharing state
3. **Async Operations**: Managing asynchronous browser interactions
4. **Error Handling**: Graceful handling of browser operations
5. **Task Sequencing**: Logical ordering of operations

#### Data Transformation Pattern

The Flow system can effectively manage data transformation pipelines, as shown in the screenshot and PDF generation examples:

```python
class Flow__Data__Transform(Type_Safe):
    @task()
    async def capture_data(self, flow_data: dict) -> None:
        raw_data = await self.source.get_data()
        flow_data['raw_data'] = raw_data

    @task()
    def transform_data(self, flow_data: dict) -> None:
        raw_data = flow_data['raw_data']
        transformed = self.transform_function(raw_data)
        flow_data['transformed'] = transformed

    @flow()
    async def execute_transformation(self) -> Flow:
        await self.capture_data()
        self.transform_data()
        return 'transformation complete'
```

Key aspects of this pattern:
1. **Data Flow**: Clear data movement between tasks
2. **State Management**: Using flow_data for intermediate results
3. **Transform Steps**: Clearly defined transformation stages
4. **Type Safety**: Leveraging Type_Safe for robust typing

### Flow Composition and Inheritance

The provided examples demonstrate effective patterns for flow composition and inheritance:

```python
class BaseWebFlow(Type_Safe):
    @task()
    async def common_setup(self):
        # Shared setup logic
        pass

class SpecificWebFlow(BaseWebFlow):
    @task()
    async def specific_operation(self):
        # Specific operation logic
        pass

    @flow()
    async def execute(self) -> Flow:
        await self.common_setup()
        await self.specific_operation()
        return 'operation complete'
```

Benefits of this approach:
1. **Code Reuse**: Common operations shared across flows
2. **Consistency**: Standardized handling of common operations
3. **Maintainability**: Clear separation of concerns
4. **Extensibility**: Easy to add new specialized flows

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