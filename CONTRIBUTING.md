# Contribution Guide

## How to Contribute

1. **Report bugs** – create Issues with a detailed description
2. **Suggest improvements** – open Issues with your proposals
3. **Write code** – submit Pull Requests

## Code Style Guidelines

### Style
- Follow PEP 8
- Maximum line length – 88 characters (Black)
- Use type hints
- Add docstrings

### Example
```python
def calculate_score(self, hand: Hand) -> int:
    """
    Calculate the total value of the hand.
    
    Args:
        hand: Hand object to calculate
        
    Returns:
        int: Total score of the hand
    """
    pass