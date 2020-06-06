package at.gattma.fh.masterthesis.parser;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;

import java.io.File;
import java.nio.file.NoSuchFileException;
import java.util.List;
import java.util.Map;

public interface ModelParser {

    List<Action> parseModel(File model) throws NoSuchFileException, ParseModelException;
    List<Action> parseModel(Map<String, String> pathMapping) throws ParseModelException;

}
