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

import org.pfred.service.exception.PFREDServiceException;
import javax.jws.WebParam;
import javax.jws.WebService;

@WebService(name = "IPFREDService", targetNamespace = "http://service.pfred.org")
public interface IPFREDService {

    public String getOrthologs(@WebParam(name = "runName") String runName, @WebParam(name = "enseblID") String enseblID, @WebParam(name = "requestedSpecies") String requestedSpecies, @WebParam(name = "species") String species) throws PFREDServiceException;

    /**
     * Return enumeration result and sequene
     * @param runName
     * @param secondaryTranscriptIDs
     * @param primaryTranscriptID
     * @param oligoLen
     * @return String array with two elements, first one is enumeration result, second one is sequence
     * @throws PFREDServiceException 
     */
    public String[] enumerate(@WebParam(name = "runName") String runName, @WebParam(name = "secondaryTranscriptIDs") String secondaryTranscriptIDs, @WebParam(name = "primaryTranscriptID") String primaryTranscriptID, @WebParam(name = "oligoLen") String oligoLen) throws PFREDServiceException;

    public String runAntisenseOffTargetSearch(@WebParam(name = "runName") String runName, @WebParam(name = "species") String species, @WebParam(name = "IDs") String IDs, @WebParam(name = "missMatches") String missMatches) throws PFREDServiceException;

    public String runsiOffTargetSearch(@WebParam(name = "runName") String runName, @WebParam(name = "species") String species, @WebParam(name = "IDs") String IDs, @WebParam(name = "missMatches") String missMatches) throws PFREDServiceException;

    public String runsiActivityModel(@WebParam(name = "runName") String runName, @WebParam(name = "primarySequence") String primarySequence) throws PFREDServiceException;

    public String runAntisenseActivityModel(@WebParam(name = "runName") String runName, @WebParam(name = "primarySequence") String primarySequence, @WebParam(name = "oligoLen") String oligoLen) throws PFREDServiceException;

    public void cleanRunDir(@WebParam(name = "runName") String runName) throws PFREDServiceException;
}
