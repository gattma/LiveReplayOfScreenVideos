package at.gattma.fh.masterthesis.parser;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.actions.ActionFactory;
import at.gattma.fh.masterthesis.actions.NullAction;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.nio.file.NoSuchFileException;
import java.util.*;

import static at.gattma.fh.masterthesis.util.Constants.TAG;

public class ModelXMLParser implements ModelParser {

    public List<Action> parseModel(File model) throws NoSuchFileException, ParseModelException {
        validateParameterOrFail(model);
        Document doc = parseModelOrFail(model);
        String path = model.getParent() + File.separator;

        NodeList setup = doc.getDocumentElement().getElementsByTagName(TAG.SETUP);
        List<Action> workflow = handleNodeList(setup, path);

        NodeList interaction = doc.getDocumentElement().getElementsByTagName(TAG.INTERACTION);
        workflow.addAll(handleNodeList(interaction, path));

        return workflow;
    }

    public List<Action> parseModel(Map<String, String> pathMapping) throws ParseModelException {
        String modelPath = pathMapping.get("workflow.xml");
        if (modelPath == null) throw new IllegalStateException("no model in mapping!");

        File model = new File(modelPath);
        Document doc = parseModelOrFail(model);

        NodeList setup = doc.getDocumentElement().getElementsByTagName(TAG.SETUP);
        List<Action> workflow = handleNodeList(setup, pathMapping);

        NodeList interaction = doc.getDocumentElement().getElementsByTagName(TAG.INTERACTION);
        workflow.addAll(handleNodeList(interaction, pathMapping));

        return workflow;
    }

    private void validateParameterOrFail(File model) throws NoSuchFileException {
        Objects.requireNonNull(model);
        if (!model.exists()) throw new NoSuchFileException("the provided file does not exist!");
    }

    private Document parseModelOrFail(File model) throws ParseModelException {
        DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder;
        try {
            dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(model);
            doc.getDocumentElement().normalize();
            return doc;
        } catch (ParserConfigurationException | SAXException | IOException e) {
            throw new ParseModelException("failed to parse the provided file", e);
        }
    }

    private List<Action> handleNodeList(NodeList list, String path) {
        if (list.getLength() == 0) return new ArrayList<>();

        List<Action> workflow = new ArrayList<>();
        NodeList actions = list.item(0).getChildNodes();
        for (int i = 0; i < actions.getLength(); i++) {
            Node action = actions.item(i);
            if (action.getNodeName().equalsIgnoreCase(TAG.ACTION)) {
                workflow.add(toAction(action, path));
            }
        }

        return workflow;
    }

    private List<Action> handleNodeList(NodeList list, Map<String, String> pathMapping) {
        if (list.getLength() == 0) return new ArrayList<>();

        List<Action> workflow = new ArrayList<>();
        NodeList actions = list.item(0).getChildNodes();
        for (int i = 0; i < actions.getLength(); i++) {
            Node action = actions.item(i);
            String val = pathMapping.get(action.getTextContent());
            if(val == null) val = action.getTextContent();

            if (action.getNodeName().equalsIgnoreCase(TAG.ACTION)
                    && action.getNodeType() == Node.ELEMENT_NODE
            ) {
                workflow.add(ActionFactory.buildAction((Element) action, val));
            }
        }
        return workflow;
    }

    private Action toAction(Node node, String path) {
        if (node.getNodeType() == Node.ELEMENT_NODE) {
            Element action = (Element) node;
            return ActionFactory.buildAction(action, String.format("%s%s", path, action.getTextContent()));
        }

        return new NullAction();
    }
}
