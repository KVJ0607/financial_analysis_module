# Financial Analysis Module

A modular Python package for advanced financial data analysis, supporting event studies, pricing data, news sentiment, and flexible group operations.

---

## Features

- **Unified Data Model:**  
  Abstract base classes for `DataPoint` and `Element` to represent financial data and their groupings.

- **Group Operations:**  
  The `Group` class supports Cayley table logic, group normalization, and joining of different data collections.

- **Extensible Visitor Pattern:**  
  Easily export or process data in various formats (CSV, JSON, etc.) using the visitor pattern.

- **Event Study Support:**  
  Built-in support for event windows, abnormal returns, and news sentiment integration.

- **Flexible Registry System:**  
  Register and manage custom element types and requirements for extensibility.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/financial_analysis_module.git
cd financial_analysis_module
pip install -r requirements.txt
```

---

## Quick Start

```python
import finGp

# Load pricing and news data
firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv", shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv", shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv", shareCode='0038.HK')

# Join news sentiment to pricing groups
firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)

# Update group elements
firstTractorA.update()
firstTractorH.update()

# Export results
csvVisitor = finGp.CsvVistor()
firstTractorA.acceptOutVisitor(csvVisitor, "output/firstTractorA.csv")
firstTractorH.acceptOutVisitor(csvVisitor, "output/firstTractorH.csv")

print("done")
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
    element/
    group_vistor/
```

- **element/**: Core data models (`DataPoint`, `Element`), element types (pricing, news, etc.), and set/convert helpers.
- **group.py**: The main `Group` class for managing and operating on collections of elements.
- **creator/**: Utilities for loading data from CSV and other sources.
- **group_vistor/**: Visitor pattern implementations for exporting or processing groups.
- **_operator/**: Operator classes for combining elements (e.g., pricing + news).

---

## Extending the Package

- **Add a new Element type:**  
  1. Subclass `Element` and `DataPoint` in `element/elements/`.
  2. Register your new class in the registry.
  3. Optionally, implement a visitor for export.

- **Add a new Visitor:**  
  1. Subclass `Visitor` in `group_vistor/visitor.py`.
  2. Implement the required visit methods.

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

## Contact

For questions or suggestions, open an issue or contact [yourname@domain.com](mailto:yourname@domain.com).
