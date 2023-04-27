import os
from collections.abc import Iterable
from .mapper_interface import MapperInterface
import csv
from typing import Union
import pkg_resources

class ICD10toICD9(MapperInterface):
    """
    Maps icd10 codes to icd9.
    
    Source of mapping: https://www.nber.org/research/data/icd-9-cm-and-icd-10-cm-and-icd-10-pcs-crosswalk-or-general-equivalence-mappings
    """
    def __init__(self):
        self.path2file = "data_sources/icd10cmtoicd9gem.csv"
        self._setup()

    def _setup(self):
        current_file_path = pkg_resources.resource_filename(__name__, '')
        filepath = os.path.join(
            os.path.dirname(
            os.path.dirname(current_file_path)),
                self.path2file
        )
        
        self.icd10_to_icd9 = self._parse_file(filepath)


    def _map_single(self, icd10code : str):
            
        try:
            return self.icd10_to_icd9[icd10code]
        except:
            return None

    def map(self,
            icd10code : Union[str, Iterable]
            ):
        """
        Given an icd10 code, returns the corresponding icd9 code.

        Parameters
        ----------

        code : str | Iterable
            icd10 code

        Returns:
            icd9 code or np.nan when the mapping is not possible
        """
            
        if isinstance(icd10code, str):
            return self._map_single(icd10code)

        elif isinstance(icd10code, Iterable):
            return [ self._map_single(c) for c in icd10code ]
        
        raise TypeError(f'Wrong input type. Expecting str or pd.Series. Got {type(icd10code)}')    


    def _parse_file(self, filepath : str):

        mapping = {}

        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            headers = next(reader)

            for row in reader:
                icd10, icd9 = row[0].strip(), row[1].strip()

                mapping[icd10] = icd9
        return mapping