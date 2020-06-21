from jinja2 import Environment, FileSystemLoader


class WorkflowBuilder:

    def __init__(self,
                 html_template='workflowHTML.MATERIAL.jinja',
                 xml_template='workflowXML.jinja',
                 sikuli_template='workflowSIKULI.jinja'):
        self.workflow = []
        file_loader = FileSystemLoader('resources/templates')
        env = Environment(loader=file_loader)

        self.template_xml = env.get_template(xml_template)
        self.template_html = env.get_template(html_template)
        self.template_sikuli = env.get_template(sikuli_template)

    def append(self, action, value, attributes=''):
        self.workflow.append(WorkflowEntry(action, value, attributes))

    def as_xml(self):
        return self.template_xml.render(actions=self.workflow)

    def as_html(self):
        return self.template_html.render(actions=self.workflow)

    def as_sikuli_script(self):
        return self.template_sikuli.render(actions=self.workflow)


class WorkflowEntry:

    def __init__(self, action, value, attributes):
        self.action = action
        self.value = value
        self.attributes = attributes
