# Financial Analysis Module

[![GitHub Repo](https://img.shields.io/github/stars/KVJ0607/financial_analysis_module?style=social)](https://github.com/KVJ0607/financial_analysis_module)

A modular Python package for advanced financial data analysis, supporting event studies, pricing data, news sentiment, and flexible group operations.

---

## Features

- **Unified Data Model:**  
  Abstract base classes for `DataPoint` and `Element` to represent financial data and their groupings.

- **Group Operations:**  
  The `Group` class supports Cayley table logic, group normalization.

<!-- - **Extensible Visitor Pattern:**  
  Easily export or process data in various formats (CSV, JSON, etc.) using the visitor pattern. -->

- **Basic Element Support:**  
  Built-in support for event windows, abnormal returns, and news sentiment integration.

- **Flexible Space Definition:**  
  Add or remove custom element types by updating the `Space` definition.

<!-- - **CSV Data Import:**  
  Use `PricingCollectionCreator` and `NewsCollectionCreator` to load pricing and news sentiment data from CSV files with customizable column mapping. -->

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/KVJ0607/financial_analysis_module.git
cd financial_analysis_module
pip install -r requirements.txt
```

---

## Quick Start

```python
import finGp
from scipy import stats

# Initialize the default space definition
finGp.Space.initDefaultSpaceDefinition()

# Load pricing and news data
firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv(
    "example_data/hshare/0038.HK.csv", shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv(
    "example_data/ashare/601038.SH.csv", shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv(
    "example_data/sentiment/test_data.csv", shareCode='0038.HK')

# Join news sentiment to pricing groups
firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)

# Update group elements
firstTractorA.update()
firstTractorH.update()

# Export results (without normalization)
firstTractorA.acceptOutVisitor(csvVisitor, "output/firstTractorA_withoutN.csv")
firstTractorH.acceptOutVisitor(csvVisitor, "output/firstTractorH_withoutN.csv")

# Normalize groups
finGp.Group.normalizeAllGroups(firstTractorA, firstTractorH)

# Export results (after normalization)
firstTractorA.acceptOutVisitor(csvVisitor, "output/firstTractorA")
firstTractorH.acceptOutVisitor(csvVisitor, "output/firstTractorH")
```

---

## Example: Customizing CSV Import

You can specify which columns in your CSV correspond to date, site address, and sentiment score:

```python
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv(
    "example_data/sentiment/test_data.csv",
    shareCode='0038.HK',
    dateIndex=0,
    siteAddressIndex=1,
    sentimentalScoreIndex=2,
    isHeading=True
)
```

---

## Adding or Removing Element Types

To add a new element type, **update the space definition** using the `Space` class:

```python
from finGp.group.space import Space
from finGp.element.elements.myNewElement import MyNewElement

# Add your new element type to the space definition
Space.addSpaceDefinition(MyNewElement)
```

To remove an element type:

```python
Space.removeSpaceDefinition(MyNewElement)
```

You can also re-initialize the space with a custom set of element types:

```python
Space.initSpaceDefinition({MyNewElement, AnotherElement, ...})
```

---

## Package Structure

```
finGp/
    __init__.py
    group.py
    _shareEntity.py
    _date_utils/
    _operator/
    creator/
        creators/
            newsCollectionCreator.py
            pricingCollectionCreator.py
    element/
    
example_data/
    hshare/
    ashare/
    sentiment/
output/
```

- **element/**: Core data models (`DataPoint`, `Element`), element types (pricing, news, etc.), and set/convert helpers.
- **group.py**: The main `Group` class for managing and operating on collections of elements.
- **creator/creators/**: Utilities for loading data from CSV and other sources.
- **_operator/**: Operator classes for combining elements (e.g., pricing + news).

---

## Extending the Package

- **Add a new Element type:**  
  1. Subclass `Element` and `DataPoint` in `element/elements/`.
  2. Update the space definition using `Space.addSpaceDefinition(MyNewElement)`.
  3. Optionally, implement a visitor for export.


---

## Contributing

Pull requests are welcome! Please open an issue first to discuss your proposed changes.

---

## License

MIT License

---

## Acknowledgements

- Inspired by event study methodology and modular financial data analysis.
- Uses [PEP 544 Protocols](https://peps.python.org/pep-0544/) for flexible type checking.

---

## Links

- [Project Repository](https://github.com/KVJ0607/financial_analysis_module)
- [Example Data](https://github.com/KVJ0607/financial_analysis_module/tree/main/example_data)

---

## Contact

For questions or suggestions, open an issue or contact [Sean Yuen](mailto:siukwanyuen@icloud.com).