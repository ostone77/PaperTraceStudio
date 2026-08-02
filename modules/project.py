class Project:
    """
    Paper Trace Studio Project

    프로젝트 하나에 필요한 정보를 보관한다.
    Build012B에서는 데이터 저장 역할만 한다.
    """

    def __init__(self):

        # Project
        self.name = ""
        self.input_file = ""
        self.output = ""

        # Output folders
        self.pen = ""
        self.cut = ""
        self.vector = ""
        self.dxf = ""
        self.svg = ""
        self.fold_candidate = ""
        self.fold_clean = ""

        # Parts
        self.parts = []