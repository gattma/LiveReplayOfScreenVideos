package at.gattma.fh.masterthesis.util;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import at.gattma.fh.masterthesis.parser.ModelParser;
import at.gattma.fh.masterthesis.parser.ModelXMLParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ArchiveHelper {

    private static ModelParser XML_PARSER = new ModelXMLParser();

    private ArchiveHelper() {
        // SINGLETON
    }

    public static List<Action> createWorkflow(File replayFile) throws ParseModelException {
        try {
            return XML_PARSER.parseModel(extractReplayFile(replayFile));
        } catch (Exception e) {
            System.err.println("Failed to extract replay file, " + e.getMessage());
            e.printStackTrace();
            throw new ParseModelException("failed to extract replay file: " + e.getMessage());
        }
    }

    private static Map<String, String> extractReplayFile(File replayFile) throws IOException {
        ZipInputStream zis = new ZipInputStream(new FileInputStream(replayFile));
        ZipEntry zipEntry = zis.getNextEntry();
        byte[] buffer = new byte[1024];

        Map<String, String> fileNameToPath = new HashMap<>();
        while (zipEntry != null) {
            File tempFile = File.createTempFile(zipEntry.getName(), ".png");
            tempFile.deleteOnExit();

            FileOutputStream fos = new FileOutputStream(tempFile);
            int len;
            while ((len = zis.read(buffer)) > 0) {
                fos.write(buffer, 0, len);
            }
            fos.close();

            fileNameToPath.put(zipEntry.getName(), tempFile.getAbsolutePath());
            zipEntry = zis.getNextEntry();
        }

        zis.closeEntry();
        zis.close();

        return fileNameToPath;
    }


    public static File findReplayFileInDir(File videoFile) {
        File[] files = videoFile.getParentFile().listFiles((dir, name) -> name.toLowerCase().endsWith(".replay"));
        assert files != null;
        return files[0];
    }

}
