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
package org.pfred.service.sample;

import org.pfred.service.PFREDServiceImpl;
import org.pfred.service.IPFREDService;
import org.pfred.service.exception.PFREDServiceException;
import org.pfred.service.model.ResultBean;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class PFREDServiceSample {

    public static void main(String[] args) {

        IPFREDService service = new PFREDServiceImpl();

        String result = getOrthologs(service);
        System.out.println("orthologs=" + result);

        ResultBean resultBean = enumerate(service);
        System.out.println("enumerate=" + resultBean.getResults()[0]);



        antisenseOffTarget(service);
        antisenseActivityModel(service);

        // siOffTarget(service);
        // siActivity(service);

        System.out.println("DONE");
    }

    private static void test() {
        //runCommandThroughShell("perl asOligoWalk.pl energy.htm 1 1 ", "/local/PFRED/runs/test");
        runCommandThroughShell("sh RNAiDesign---siRNAOffTargetSearchwithBowtie.sh human ENST00000378474 2", "/local/PFRED/runs/test");
        //              runCommandThroughShell("perl asOligoWalk.pl energy.htm 1 1 >foo.txt", "/local/PFRED/runs/test");

        System.out.println("DONE");
    }

    private static boolean runCommandThroughShell(String command, String directory) {
        File wd = new File("/bin");
        System.out.println(wd);
        Process proc = null;
        try {
            proc = Runtime.getRuntime().exec("/bin/bash", null, wd);
        } catch (IOException e) {
            e.printStackTrace();
        }
        if (proc != null) {
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(proc.getOutputStream())), true);

            out.println("cd " + directory);
            //    out.println("ls");
            out.println(command);
            out.println("exit");
            out.flush();
            try {
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                //   Logger.getLogger(PFREDServiceImpl.class.getName()).log(Level.SEVERE, null, ex);
            }
            try {
                String line;
                while ((line = in.readLine()) != null) {
                    System.out.println(line);
                }
                proc.waitFor();
                in.close();
                out.close();
                proc.destroy();
            } catch (Exception e) {
                e.printStackTrace();
                return false;
            }
        }
        return true;
    }

    private static String getOrthologs(IPFREDService service) {
        try {
            String orthologs = "";

            // orthologs = service.getOrthologs("test", "ENSG00000165175", "rat,mouse", "human");
            orthologs = service.getOrthologs("test", "ENST00000227667", "rat,mouse", "human");

            return orthologs;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static ResultBean enumerate(IPFREDService service) {
        try {

            //  ResultBean resultBean = service.enumerate("test", "ENST00000378474,ENST00000336949,ENSRNOT00000004305,ENSMUST00000115524,ENSMUST00000008179", "ENST00000336949", "19");
            ResultBean resultBean = service.enumerate("test", "ENST00000375345,ENST00000227667,ENSMUST00000118649,ENSMUST00000034586,ENSMUST00000121916", "ENST00000375345", "19");


            return resultBean;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static String siOffTarget(IPFREDService service) {
        try {


            // String result = service.runsiOffTargetSearch("test", "human,rat", "ENST00000378474,ENSRNOT00000004305", "2");
            String result = service.runsiOffTargetSearch("test", "human,mouse", "ENST00000375345,ENSMUST00000118649", "2");
            //

            System.out.println("siOffTarget=" + result);

            return result;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static String antisenseOffTarget(IPFREDService service) {
        try {


            // String result = service.runAntisenseOffTargetSearch("test", "human", "ENST00000378474", "2");
            String result = service.runAntisenseOffTargetSearch("test", "human,mouse", "ENST00000375345,ENSMUST00000118649", "2");

            System.out.println("siOffTarget=" + result);

            return result;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static String siActivity(IPFREDService service) {
        try {


            //String result = service.runsiActivityModel("test", "GGCTCACTCTGCAACCAAGGCACGTGCATTCTGGTCATCCCACGCGGGGAGCGCGCGCAAGGCCCGCCCAGCCCCCACATGCCAGCCCCACCCTCCAGTCGGTCCGGACGCCGACGCCTTTTTGACCCTCGCTGTGCCCGGCCCTCCTCATCTGGCCTGCCCAGGGCTTGGTGCTGGCGGGGTCCAGCTGCTCCAATCCCTCCTCCTCTGCTCTGCCCTGCCCTGCCCTGGCCTGCCCCGGCGCCCTCCCTCAGCCCGGGTATCAGGCGAGAGGCGGAGCTGGCCCGGCGCGCCCCGCCCCCGCTGTAGAAAGGGCCGGGCGAGTGTTACTCGCGGTCATCCCGGCCTGGGCCTTTTATCTCGGTGCTGCCGGGGGAGGCGGGAGGAGGAGACACCAGGGGTGGCCCTGAGCGCCGGCGACACCTTTCCTGGACTATAAATTGAGCACCTGGGATGGGTAGGGGGCCAACGCAGTCACCGCCGTCCGCAGTCACAGTCCAGCCACTGACCGCAGCAGCGCCCTTGCGTAGCAGCCGCTTGCAGCGAGAACACTGAATTGCCAACGAGCAGGAGAGTCTCAAGGCGCAAGAGGAGGCCAGGGCTCGACCCACAGAGCACCCTCAGCCATCGCGAGTTTCCGGGCGCCAAAGCCAGGAGAAGCCGCCCATCCCGCAGGGCCGGTCTGCCAGCGAGACGAGAGTTGGCGAGGGCGGAGGAGTGCCGGGAATCCCGCCACACCGGCTATAGCCAGGCCCCCAGCGCGGGCCTTGGAGAGCGCGTGAAGGCGGGCATCCCCTTGACCCGGCCGACCATCCCCGTGCCCCTGCGTCCCTGCGCTCCAACGTCCGCGCGGCCACCATGATGCAAATCTGCGACACCTACAACCAGAAGCACTCGCTCTTTAACGCCATGAATCGCTTCATTGGCGCCGTGAACAACATGGACCAGACGGTGATGGTGCCCAGCTTGCTGCGCGACGTGCCCCTGGCTGACCCCGGGTTAGACAACGATGTTGGCGTGGAGGTAGGCGGCAGTGGCGGCTGCCTGGAGGAGCGCACGCCCCCAGTCCCCGACTCGGGAAGCGCCAATGGCAGCTTTTTCGCGCCCTCTCGGGACATGTACAGCCACTACGTGCTTCTCAAGTCCATCCGCAACGACATCGAGTGGGGGGTCCTGCACCAGCCGCCTCCACCGGCTGGGAGCGAGGAGGGCAGTGCCTGGAAGTCCAAGGACATCCTGGTGGACCTGGGCCACTTGGAGGGTGCGGACGCCGGCGAAGAAGACCTGGAACAGCAGTTCCACTACCACCTGCGCGGGCTGCACACTGTGCTCTCGAAACTCACGCGCAAAGCCAACATCCTCACTAACAGATACAAGCAGGAGATCGGCTTCGGCAATTGGGGCCACTGAGGCGTGGCGCCCGTGGCTGCCCAGCACCTTCTTCGACCCATCTCACCCTCTCTCATTCCTCAAAGCTTTTTTTTTTTTTCCTGGCTGGGGGGCGGGAAGGGCAGACTGCAAACTGGGGGGCTGCGTACGTGCAGGAGGCGCGGTGGGGCTGCGTGGAGGAGGGGGCCACGTGTGAGAGAGAAGAAAATGGTGGCCGGAGATGGGAGGGCCCAAGGAACCTCCTGGGAGGGGGCCTGCATTCTATGTTGGTGGGAATGGGACTGGGCTGACGCCCTGCATTCAGCCTGTGCCTTTCCTGGGGTTTCTTTTCTGTTCTTTTCGGAGGAGAGGGCCCGAGAAGGGGCCATACCAGGGCGCGGCGCTGGGTTGCCACACTTGGGAAAGCAGCCCGGAGCTGGGTGCTGGGGAAGGCGGGGCGCGTAGCCTCCCGCCGCCCTGCGGTTGGGCCGGTGGAGGCCCAGGCGTTGCTAGGATTGCATCAGTTTTCCTGTTTGCACTATTTCTTTTTGTAACATTGGCCCTGTGTGAAGTATTTCGAATCTCCTCCTTGCTCTGAAACTTCAGCGATTCCATTGTGATAAGCGCACAAACAGCACTGTCTGTCGGTAATCGGTACTACTTTATTAATGATTTTCTGTTACACTGTATAGTAGTCCTATGGCACCCCCACCCCATCCCTTTCGTGCCACTCCCGTCCCCACCCCCACCCCAGTGTGTATAAGCTGGCATTTCGCCAGCTTGTACGTAGCTTGCCACTCAGTGAAAATAATAACATTATTATGAGAAAGTGGACTTAACCGAAATGGAACCAACTGACATTCTATCGTGTTGTACATAGAATGATGAAGGGTTCCACTGTTGTTGTATGTCTTAAATTTATTTAAAACTTTTTTTAATCCAGATGTAGACTATATTCTAAAAAATAAAAAAGCAAATGTGTCAACTAAATTGGACAAGCGTCTGGTCCTCATTAATCTGCCAATGAATGGTTTCGTCATTAAATAAAAATCAATTTAATTGATTTACTAGC");

            String result = service.runsiActivityModel("test", "TTCATCCCTAGAGGCAGCTGCTCCAGGGGCCACGCCACCTCCCCAGGGAGGGGTCCAGAGGCATGGGGACCTGGGGTGCCCCTCACAGGACACTTCCTTGCAGGAACAGAGGTGCCATGCAGCCCCGGGTACTCCTTGTTGTTGCCCTCCTGGCGCTCCTGGCCTCTGCCCGAGCTTCAGAGGCCGAGGATGCCTCCCTTCTCAGCTTCATGCAGGGTTACATGAAGCACGCCACCAAGACCGCCAAGGATGCACTGAGCAGCGTGCAGGAGTCCCAGGTGGCCCAGCAGGCCAGGGGCTGGGTGACCGATGGCTTCAGTTCCCTGAAAGACTACTGGAGCACCGTTAAGGACAAGTTCTCTGAGTTCTGGGATTTGGACCCTGAGGTCAGACCAACTTCAGCCGTGGCTGCCTGAGACCTCAATACCCCAAGTCCACCTGCCTATCCATCCTGCGAGCTCCTTGGGTCCTGCAATCTCCAGGGCTGCCCCTGTAGGTTGCTTAAAAGGGACAGTATTCTCAGTGCTCTCCTACCCCACCTCATGCCTGGCCCCCCTCCAGGCATGCTGGCCTCCCAATAAAGCTGGACAAGAAGCTGCTATGA");
            System.out.println("siActivity=" + result);

            return result;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static String antisenseActivityModel(IPFREDService service) {
        try {


//            String result = service.runAntisenseActivityModel("test", "GGCTCACTCTGCAACCAAGGCACGTGCATTCTGGTCATCCCACGCGGGGAGCGCGCGCAAGGCCCGCCCAGCCCCCACATGCCAGCCCCACCCTCCAGTCGGTCCGGACGCCGACGCCTTTTTGACCCTCGCTGTGCCCGGCCCTCCTCATCTGGCCTGCCCAGGGCTTGGTGCTGGCGGGGTCCAGCTGCTCCAATCCCTCCTCCTCTGCTCTGCCCTGCCCTGCCCTGGCCTGCCCCGGCGCCCTCCCTCAGCCCGGGTATCAGGCGAGAGGCGGAGCTGGCCCGGCGCGCCCCGCCCCCGCTGTAGAAAGGGCCGGGCGAGTGTTACTCGCGGTCATCCCGGCCTGGGCCTTTTATCTCGGTGCTGCCGGGGGAGGCGGGAGGAGGAGACACCAGGGGTGGCCCTGAGCGCCGGCGACACCTTTCCTGGACTATAAATTGAGCACCTGGGATGGGTAGGGGGCCAACGCAGTCACCGCCGTCCGCAGTCACAGTCCAGCCACTGACCGCAGCAGCGCCCTTGCGTAGCAGCCGCTTGCAGCGAGAACACTGAATTGCCAACGAGCAGGAGAGTCTCAAGGCGCAAGAGGAGGCCAGGGCTCGACCCACAGAGCACCCTCAGCCATCGCGAGTTTCCGGGCGCCAAAGCCAGGAGAAGCCGCCCATCCCGCAGGGCCGGTCTGCCAGCGAGACGAGAGTTGGCGAGGGCGGAGGAGTGCCGGGAATCCCGCCACACCGGCTATAGCCAGGCCCCCAGCGCGGGCCTTGGAGAGCGCGTGAAGGCGGGCATCCCCTTGACCCGGCCGACCATCCCCGTGCCCCTGCGTCCCTGCGCTCCAACGTCCGCGCGGCCACCATGATGCAAATCTGCGACACCTACAACCAGAAGCACTCGCTCTTTAACGCCATGAATCGCTTCATTGGCGCCGTGAACAACATGGACCAGACGGTGATGGTGCCCAGCTTGCTGCGCGACGTGCCCCTGGCTGACCCCGGGTTAGACAACGATGTTGGCGTGGAGGTAGGCGGCAGTGGCGGCTGCCTGGAGGAGCGCACGCCCCCAGTCCCCGACTCGGGAAGCGCCAATGGCAGCTTTTTCGCGCCCTCTCGGGACATGTACAGCCACTACGTGCTTCTCAAGTCCATCCGCAACGACATCGAGTGGGGGGTCCTGCACCAGCCGCCTCCACCGGCTGGGAGCGAGGAGGGCAGTGCCTGGAAGTCCAAGGACATCCTGGTGGACCTGGGCCACTTGGAGGGTGCGGACGCCGGCGAAGAAGACCTGGAACAGCAGTTCCACTACCACCTGCGCGGGCTGCACACTGTGCTCTCGAAACTCACGCGCAAAGCCAACATCCTCACTAACAGATACAAGCAGGAGATCGGCTTCGGCAATTGGGGCCACTGAGGCGTGGCGCCCGTGGCTGCCCAGCACCTTCTTCGACCCATCTCACCCTCTCTCATTCCTCAAAGCTTTTTTTTTTTTTCCTGGCTGGGGGGCGGGAAGGGCAGACTGCAAACTGGGGGGCTGCGTACGTGCAGGAGGCGCGGTGGGGCTGCGTGGAGGAGGGGGCCACGTGTGAGAGAGAAGAAAATGGTGGCCGGAGATGGGAGGGCCCAAGGAACCTCCTGGGAGGGGGCCTGCATTCTATGTTGGTGGGAATGGGACTGGGCTGACGCCCTGCATTCAGCCTGTGCCTTTCCTGGGGTTTCTTTTCTGTTCTTTTCGGAGGAGAGGGCCCGAGAAGGGGCCATACCAGGGCGCGGCGCTGGGTTGCCACACTTGGGAAAGCAGCCCGGAGCTGGGTGCTGGGGAAGGCGGGGCGCGTAGCCTCCCGCCGCCCTGCGGTTGGGCCGGTGGAGGCCCAGGCGTTGCTAGGATTGCATCAGTTTTCCTGTTTGCACTATTTCTTTTTGTAACATTGGCCCTGTGTGAAGTATTTCGAATCTCCTCCTTGCTCTGAAACTTCAGCGATTCCATTGTGATAAGCGCACAAACAGCACTGTCTGTCGGTAATCGGTACTACTTTATTAATGATTTTCTGTTACACTGTATAGTAGTCCTATGGCACCCCCACCCCATCCCTTTCGTGCCACTCCCGTCCCCACCCCCACCCCAGTGTGTATAAGCTGGCATTTCGCCAGCTTGTACGTAGCTTGCCACTCAGTGAAAATAATAACATTATTATGAGAAAGTGGACTTAACCGAAATGGAACCAACTGACATTCTATCGTGTTGTACATAGAATGATGAAGGGTTCCACTGTTGTTGTATGTCTTAAATTTATTTAAAACTTTTTTTAATCCAGATGTAGACTATATTCTAAAAAATAAAAAAGCAAATGTGTCAACTAAATTGGACAAGCGTCTGGTCCTCATTAATCTGCCAATGAATGGTTTCGTCATTAAATAAAAATCAATTTAATTGATTTACTAGC", "19");

            String result = service.runAntisenseActivityModel("test", "TTCATCCCTAGAGGCAGCTGCTCCAGGGGCCACGCCACCTCCCCAGGGAGGGGTCCAGAGGCATGGGGACCTGGGGTGCCCCTCACAGGACACTTCCTTGCAGGAACAGAGGTGCCATGCAGCCCCGGGTACTCCTTGTTGTTGCCCTCCTGGCGCTCCTGGCCTCTGCCCGAGCTTCAGAGGCCGAGGATGCCTCCCTTCTCAGCTTCATGCAGGGTTACATGAAGCACGCCACCAAGACCGCCAAGGATGCACTGAGCAGCGTGCAGGAGTCCCAGGTGGCCCAGCAGGCCAGGGGCTGGGTGACCGATGGCTTCAGTTCCCTGAAAGACTACTGGAGCACCGTTAAGGACAAGTTCTCTGAGTTCTGGGATTTGGACCCTGAGGTCAGACCAACTTCAGCCGTGGCTGCCTGAGACCTCAATACCCCAAGTCCACCTGCCTATCCATCCTGCGAGCTCCTTGGGTCCTGCAATCTCCAGGGCTGCCCCTGTAGGTTGCTTAAAAGGGACAGTATTCTCAGTGCTCTCCTACCCCACCTCATGCCTGGCCCCCCTCCAGGCATGCTGGCCTCCCAATAAAGCTGGACAAGAAGCTGCTATGA", "19");

            System.out.println("antisenseActivity=" + result);

            return result;
        } catch (PFREDServiceException ex) {
            ex.printStackTrace();
        }
        return null;
    }
}
