# Financial Analysis Module

A modular Python package for advanced financial data analysis, supporting event studies and flexible group operations.  
**Supports Car3, Pricing, and News Sentiment data as core Element types, and is designed to be easily extended by users.**

---

## Features

- **Core Element Types:**  
  Built-in support for Car3, Pricing, and News Sentiment data as first-class Elements.

- **Group Operations:**  
  The `Group` class enables normalization, joining, and updating of collections of Elements.

- **Extensible Architecture:**  
  Easily add your own custom Element types and extend the package for new financial data domains.

---

## Installation

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

# Initialize the default space definition (Car3, Pricing, News Sentiment)
finGp.Space.initDefaultSpaceDefinition()

# Load pricing and news sentiment data
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

# Export results before normalization
firstTractorA.acceptOutVisitor("output/firstTractorA_withoutN.csv")
firstTractorH.acceptOutVisitor("output/firstTractorH_withoutN.csv")

# Normalize groups
finGp.Group.normalizeAllGroups(firstTractorA, firstTractorH)

# Export results after normalization
firstTractorA.acceptOutVisitor("output/firstTractorA")
firstTractorH.acceptOutVisitor("output/firstTractorH")
```

---

## Extending the Package

You can add your own custom Element types and include them in the analysis by updating the space definition:

```python
from finGp.group.space import Space
from finGp.element.elements.myNewElement import MyNewElement

Space.addSpaceDefinition(MyNewElement)
```

You can also define **custom operations between Element types** by subclassing the `Operator` class:

```python
from finGp.operation.operator import Operator

class MyCustomOperator(Operator):
    @classmethod
    def getProductClass(cls):
        # Return the resulting Element type
        return MyResultElement

    @classmethod
    def getOperands(cls):
        # Return a set of operand Element types
        return {MyElementA, MyElementB}

    @classmethod
    def dot(cls, *operands):
        # Implement the logic to combine operands into a new Element
        ...
```



---

## Project Structure

```
finGp/
    creator/
    element/
    group/
    operation/
    ...
```

---

## License

MIT License

---

## Contact

For questions or suggestions, open an issue or contact [Sean Yuen](mailto:siukwanyuen@icloud.com).