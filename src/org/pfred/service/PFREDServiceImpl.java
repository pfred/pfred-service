/*
 *  PFRED: A computational tool for siRNA and antisense design
 *  Copyright (C) 2011 Pfizer, Inc.
 *
 *  This file is part of the PFRED software.
 *
 *  PFRED is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package org.pfred.service;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.jws.WebParam;
import javax.jws.WebService;
import javax.servlet.http.HttpServletRequest;
import org.codehaus.xfire.MessageContext;
import org.codehaus.xfire.service.invoker.AbstractInvoker;
import org.codehaus.xfire.transport.http.XFireServletController;
import org.pfred.service.exception.PFREDServiceException;
import org.pfred.service.model.ResultBean;

@WebService(name = "IPFREDService", targetNamespace = "http://service.pfred.org")
public class PFREDServiceImpl implements IPFREDService {

    private static Logger logger = Logger.getLogger(PFREDServiceImpl.class.getName());
    private static String runDirectory = System.getenv("RUN_DIR");

    @Override
    public String getOrthologs(@WebParam(name = "runName") String runName, @WebParam(name = "enseblID") String enseblID, @WebParam(name = "requestedSpecies") String requestedSpecies, @WebParam(name = "species") String species) throws PFREDServiceException {
        logRemoteHost("getOrthologs");

        String fullRunDirectory = prepareRunDir(runName);
        String outputFilePath = fullRunDirectory + "/seqAnnotation.csv";
        String command = "getOrthologs.sh  " + enseblID + " " + species + " " + requestedSpecies + " " + outputFilePath;

        boolean success = runCommandThroughShell(command, fullRunDirectory);
        String returnValue = "";
        if (success) {
            logger.info("Shell command run successfully");
            try {
                returnValue = readFileAsString(outputFilePath);
            } catch (IOException ex) {
                logger.log(Level.SEVERE, "Error reading file: " + outputFilePath, ex);
            }
        } else {
            logger.info("Shell command run failed");
        }
        return returnValue;
    }

    @Override
    public ResultBean enumerate(@WebParam(name = "runName") String runName, @WebParam(name = "secondaryTranscriptIDs") String secondaryTranscriptIDs, @WebParam(name = "primaryTranscriptID") String primaryTranscriptID, @WebParam(name = "oligoLen") String oligoLen) throws PFREDServiceException {
        logRemoteHost("enumerate");

        String fullRunDirectory = prepareRunDir(runName);

        String command = "RnaEnumerator.sh  " + secondaryTranscriptIDs + " " + primaryTranscriptID + " " + oligoLen + "";

        boolean success = runCommandThroughShell(command, fullRunDirectory);

        ResultBean resultBean = new ResultBean();
        if (success) {
            logger.info("Shell command run successfully");
            String results[] = new String[2];
            try {
                results[0] = readFileAsString(fullRunDirectory + "/outputSummary.csv");

            } catch (IOException ex) {
                logger.log(Level.SEVERE, "Error reading file outputSummary.csv", ex);
            }

            try {
                results[1] = readFileAsString(fullRunDirectory + "/sequence.fa");
            } catch (IOException ex) {
                logger.log(Level.SEVERE, "Error reading file sequence.fa", ex);
            }

            resultBean.setResults(results);
        } else {
            logger.info("Shell command run failed");
        }

        return resultBean;
    }
    
    @Override
    public String runsiOffTargetSearch(@WebParam(name = "runName") String runName, @WebParam(name = "species") String species, @WebParam(name = "IDs") String IDs, @WebParam(name = "missMatches") String missMatches) throws PFREDServiceException {
        logRemoteHost("runsiOffTargetSearch");

        String fullRunDirectory = prepareRunDir(runName);

        String command = "RNAiDesign---siRNAOffTargetSearchwithBowtie.sh " + species + " " + IDs + " " + missMatches;

        boolean success = runCommandThroughShell(command, fullRunDirectory);
        String returnValue = "";
        if (success) {
            logger.info("Shell command run successfully");
            try {
                returnValue = readFileAsString(fullRunDirectory + "/outputSummary.csv");
            } catch (IOException ex) {
                logger.log(Level.SEVERE, "Error reading file: " + fullRunDirectory + "/outputSummary.csv", ex);
            }
        } else {
            logger.info("Shell command run failed");
        }
        return returnValue;      
    }

    @Override
    public String runsiActivityModel(@WebParam(name = "runName") String runName, @WebParam(name = "primarySequence") String primarySequence) throws PFREDServiceException {
        logRemoteHost("runsiActivityModel");

        String fullRunDirectory = prepareRunDir(runName);

        saveStringAsFile(fullRunDirectory + "/target.txt", primarySequence);

        String command = "RNAiDesignEfficacySVMmodel19mers.csh";

        boolean success = runCommandThroughShell(command, fullRunDirectory);
        String returnValue = "";
        if (success) {
            logger.info("Shell command run successfully");
            try {
                returnValue = readFileAsString(fullRunDirectory + "/outputSummary.csv");
            } catch (IOException ex) {
                logger.log(Level.SEVERE, "Error reading file: " + fullRunDirectory + "/outputSummary.csv", ex);
            }
        } else {
            logger.info("Shell command run failed");
        }
        return returnValue;
    }

    @Override
    public String runAntisenseActivityModel(@WebParam(name = "runName") String runName, @WebParam(name = "primarySequence") String primarySequence, @WebParam(name = "oligoLen") String oligoLen) throws PFREDServiceException {
        logRemoteHost("runAntisenseActivityModel");
        String fullRunDirectory = runDirectory + '/' + runName;

        saveStringAsFile(fullRunDirectory + "/target.seq", primarySequence);

        String command = "RNAiDesign---antisenseScore1.sh " + oligoLen;

        runCommandThroughShell(command, fullRunDirectory);

        try {
            String result = readFileAsString(fullRunDirectory + "/outputSummary.csv");
            return result;
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error reading file outputSummary.csv", ex);
            return "";
        }
    }

    private boolean runCommandThroughShell(String command, String directory) {
        logger.log(Level.INFO, "Running Shell Command: " + command);
        File wd = new File("/bin");
        Process proc = null;
        try {
            proc = Runtime.getRuntime().exec("/bin/bash", null, wd);
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error executing /bin/bash", ex);
            return false;
        }
        if (proc != null) {
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(proc.getOutputStream())), true);

            out.println("cd " + directory);

            out.println(command);
            out.println("exit");
            out.flush();
            try {
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                logger.log(Level.SEVERE, null, ex);
            }
            try {
                String line;
                while ((line = in.readLine()) != null) {
                    logger.info(line);
                }
                proc.waitFor();
                in.close();
                out.close();
                proc.destroy();
            } catch (Exception ex) {
                logger.log(Level.SEVERE, "Error executing command line in bash shell", ex);
                return false;
            }
        }
        return true;
    }

    @Override
    public String runAntisenseOffTargetSearch(@WebParam(name = "runName") String runName, @WebParam(name = "species") String species, @WebParam(name = "IDs") String IDs, @WebParam(name = "missMatches") String missMatches) throws PFREDServiceException {
        logRemoteHost("runAntisenseOffTargetSearch");

        String fullRunDirectory = runDirectory + '/' + runName;

        String command = "RNAiDesign---antisenseOffTargetSearchwithBowtie.sh " + species + " " + IDs + " " + missMatches;


        runCommandThroughShell(command, fullRunDirectory);


        try {
            String result = readFileAsString(fullRunDirectory + "/outputSummary.csv");
            return result;
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error reading file outputSummary.csv", ex);
            return "";
        }
    }

    @Override
    public void cleanRunDir(@WebParam(name = "runName") String runName) throws PFREDServiceException {
        logRemoteHost("cleanRunDir");
        String fullRunDirectory = runDirectory + '/' + runName;
        removeDir(fullRunDirectory);
    }

    private String readFileAsString(String filePath) throws java.io.IOException {
        StringBuffer fileData = new StringBuffer(1000);
        BufferedReader reader = new BufferedReader(new FileReader(filePath));
        char[] buf = new char[1024];
        int numRead = 0;
        while ((numRead = reader.read(buf)) != -1) {
            String readData = String.valueOf(buf, 0, numRead);
            fileData.append(readData);
            buf = new char[1024];
        }
        reader.close();
        return fileData.toString();
    }

    private static void saveStringAsFile(String filePath, String contents) {
        try {
            BufferedWriter out = new BufferedWriter(new FileWriter(filePath));
            out.write(contents);
            out.close();

        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error saving string as file", ex);
        }
    }

    private boolean copyScript(String scriptPath, String runDirectory) {
        File file = new File(runDirectory);
        try {
            Runtime.getRuntime().exec("cp " + scriptPath + " .", null, file);
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error copying script", ex);
            return false;
        }
        return true;

    }

    private String prepareRunDir(String runName) {
        String fullRunDirectory = runDirectory + '/' + runName;
        File dirFile = new File(fullRunDirectory);
        if (!dirFile.exists()) {
            dirFile.mkdir();;
        }
        return fullRunDirectory;
    }

    private boolean removeDir(String dirPath) {
        logger.info("Removing run directory: " + dirPath);
        try {
            Runtime.getRuntime().exec("rm -rf " + dirPath);
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Error removing directory: " + dirPath, ex);
            return false;
        }
        return true;

    }

    private void logRemoteHost(String methodName) {
        MessageContext mctx = AbstractInvoker.getContext();
        if (null != mctx) {
            HttpServletRequest req = (HttpServletRequest) mctx.getProperty(XFireServletController.HTTP_SERVLET_REQUEST);
            String remoteHost = req.getRemoteHost();
            logger.info(methodName + " called from " + remoteHost);
        } else {
            logger.info(methodName + " called locally");
        }

    }
}
