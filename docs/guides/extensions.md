---
title: Extensions
---

# Extensions

Strawberry provides support for adding extensions. Extensions can be used to
hook into different parts of the GraphQL execution and to provide additional
results to the GraphQL response.

To enable extensions you can pass them when creating a schema, here's an example
that enables the Apollo tracing extension:

```python
from strawberry.extensions.tracing import ApolloTracingExtension

schema = strawberry.Schema(query=Query, extensions=[ApolloTracingExtension])
```

## Creating custom extensions

To create a custom extensions you can use extend from our `Extension` base
class:

```python
from strawberry.extensions import Extension

class MyExtension(Extension):
    def get_results(self):
        return {
            "example": "this is an example for an extension"
        }

schema = strawberry.Schema(query=Query, extensions=[MyExtension])
```

## Hooks

### Request

`on_request_start` and `on_request_end` can be used to run code when a GraphQL
request starts and end, it also allows you to get the execution context

```python
from strawberry.extensions import Extension

class MyExtension(Extension):
    def on_request_start(self):
        print('GraphQL request start')

    def on_request_end(self):
        print('GraphQL request end')
```

### Resolve

`resolve` can be used to run code before or after the execution of resolvers,
this method _must_ call `_next` with all the arguments, as they will be needed
by the resolvers:

```python
from strawberry.types import Info
from strawberry.extensions import Extension

class MyExtension(Extension):
    def resolve(self, _next, root, info: Info, *args, **kwargs):
        return _next(root, info, *args, **kwargs)
```

### Get results

`get_results` allows to return a dictionary of data that will be included in the
GraphQL response.

```python
from strawberry.extensions import Extension

class MyExtension(Extension):
    def get_results(self) -> Dict[str, Any]:
        return {}
```

### Validation

`on_validation_start` and `on_validation_end` can be used to run code on the
validation step of the GraphQL execution.

```python
from strawberry.extensions import Extension

class MyExtension(Extension):
    def on_validation_start(self):
        print('GraphQL validation start')

    def on_validation_end(self):
        print('GraphQL validation end')
```

### Parsing

`on_parsing_start` and `on_parsing_end` can be used to run code on the
parsing step of the GraphQL execution.

```python
from strawberry.extensions import Extension

class MyExtension(Extension):
    def on_parsing_start(self):
        print('GraphQL parsing start')

    def on_parsing_end(self):
        print('GraphQL parsing end')
```

### Execution Context

The `Extension` object has a `execution_context` property on `self` of type `ExecutionContext`. This object can be used to gain access to additional graphql context, or request context. See the [`ExecutionContext` type](https://github.com/strawberry-graphql/strawberry/blob/main/strawberry/types/execution.py) for available data.

```python
from strawberry.extensions import Extension

from mydb import get_db_session

class MyExtension(Extension):
    def on_request_start(self):
        self.execution_context.context["db"] = get_db_session()

    def on_request_end(self):
        self.execution_context.context["db"].close()
```
