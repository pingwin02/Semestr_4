package pl.edu.pg.kask.pt;

import org.apache.commons.lang3.tuple.Pair;

import javax.imageio.ImageIO;
import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class App {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: App <directory> ");
            return;
        }

        String inputDirectory = args[0];
        String outputDirectory = inputDirectory + "_out";

        File outputDir = new File(outputDirectory);
        if (!outputDir.exists()) outputDir.mkdir();

        List<Path> imagePaths;
        Path source = Path.of(inputDirectory);
        try (Stream<Path> stream = Files.list(source)) {
            imagePaths = stream.collect(Collectors.toList());

            long time = System.currentTimeMillis();

            ForkJoinPool forkJoinPool = new ForkJoinPool(20);
            forkJoinPool.submit(() -> imagePaths.parallelStream()
                    .map(App::processImage)
                    .forEach(pair -> saveImage(pair, outputDirectory))).get();

            System.out.println("Image processing completed.");
            System.out.println("Time: " + (System.currentTimeMillis() - time) + " ms");

            forkJoinPool.shutdown();
        } catch (IOException |
                 InterruptedException |
                 ExecutionException e) {
            e.printStackTrace();
        }


    }

    private static Pair<String, BufferedImage> processImage(Path imagePath) {
        String fileName = imagePath.getFileName().toString();

        try {
            BufferedImage originalImage = ImageIO.read(imagePath.toFile());
            if (originalImage == null) {
                System.out.println("Error reading image: " + fileName);
                return null;
            }
            BufferedImage transformedImage = transformImage(originalImage);
            return Pair.of(fileName, transformedImage);
        } catch (IOException e) {
            System.out.println("Error processing image: " + fileName);
            e.printStackTrace();
            return null;
        }
    }

    private static BufferedImage transformImage(BufferedImage originalImage) {
        BufferedImage transformedImage = new BufferedImage(
                originalImage.getWidth(),
                originalImage.getHeight(),
                originalImage.getType()
        );

        for (int i = 0; i < originalImage.getWidth(); i++) {
            for (int j = 0; j < originalImage.getHeight(); j++) {
                int rgb = originalImage.getRGB(i, j);
                Color color = new Color(rgb);

                // Przykładowa zamiana składowej zielonej z niebieską
                int red = color.getRed();
                int blue = color.getBlue();
                int green = color.getGreen();
                Color outColor = new Color(red, blue, green);

                int outRgb = outColor.getRGB();
                transformedImage.setRGB(i, j, outRgb);
            }
        }

        return transformedImage;
    }

    private static void saveImage(Pair<String, BufferedImage> imagePair, String outputDirectory) {
        String fileName = imagePair.getLeft();
        BufferedImage image = imagePair.getRight();

        try {
            File outputFile = new File(outputDirectory, fileName);
            ImageIO.write(image, "jpg", outputFile);
            System.out.println("Saved image: " + fileName);
        } catch (IOException e) {
            System.out.println("Error saving image: " + fileName);
            e.printStackTrace();
        }
    }
}
