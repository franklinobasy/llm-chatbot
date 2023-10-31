
from chatbot_v2.templates.templates import (
    clean_template,
)
from chatbot_v2.handlers.base_handler import (
    BaseHandler,
    section_templates
)


class TemplateHandler(BaseHandler):
    '''Templates handler'''
    def __init__(self, section_type):
        super().__init__(section_type)

    @property
    def section(self):
        return self._section_template

    @section.setter
    def section(self, section_type: str):
        if section_type not in section_templates.keys():
            raise ValueError(
                f"This section type: \"{section_type}\" is not supported.\
                \nAvailable supported sections are: {list(section_templates.keys())}"
            )
        self.__section_template = section_templates.get(section_type)

    def get_templates(self):
        templates = []
        for template_info in self._section_template[0].items():
            clean_template_info = clean_template(template_info)
            template = clean_template_info[1][1]
            templates.append(template)
        return templates

    def get_summaries(self):
        summaries = []
        for template_info in self._section_template[0].items():
            clean_template_info = clean_template(template_info)
            summary = clean_template_info[1][0]
            summaries.append(summary)
        return summaries

    def get_template_data(self):
        templates_data = []
        templates = self.get_templates()
        sumaries = self.get_summaries()

        for summary, template in zip(sumaries, templates):
            templates_data.append(
                {
                    "summary": summary,
                    "template": template
                }
            )
        return templates_data
