# Rich

## Install

```cmd
pip install rich
```

## Used

```python
from rich.console import Console
from rich.table import Table
# Rich Console إعداد الـ
console = Console()

name   = 'Hossam Rashad'
errors   = False

console.print(f"[bold green]Successfully: {name}[/bold green]")
console.print(f"[bold red]Failed Errors: {errors}[/bold red]")

console.print(table)
```
