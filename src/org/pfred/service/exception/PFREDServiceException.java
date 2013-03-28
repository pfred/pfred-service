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
package org.pfred.service.exception;

import javax.xml.namespace.QName;
import org.codehaus.xfire.fault.FaultInfoException;


public class PFREDServiceException extends FaultInfoException {

    private PFREDServiceExceptionDetail faultDetail;

    public PFREDServiceException(String msg, PFREDServiceExceptionDetail detail) {
        super(msg);
        faultDetail = detail;
    }

    public PFREDServiceExceptionDetail getFaultInfo() {
        return faultDetail;
    }

    public static QName getFaultName() {
        return new QName("http://exception.pfred.org", "PFREDServiceFault");
    }
}
