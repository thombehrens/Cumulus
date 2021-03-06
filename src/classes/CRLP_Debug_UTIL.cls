/*
    Copyright (c) 2018, Salesforce.org
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Salesforce.org nor the names of
      its contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
*/
/**
* @author Salesforce.org
* @date 2018
* @group Customizable Rollups Debug Logger
* @description Simple debugging utilty for Customizable Rollups. The CRLP_Debug_UTIL.setCurrentRollupState() method
* is called periodically throughout the code to store data in a static list<> var. The getCurrentRollupState() method
* returns a concatenated version of that list as a single string. Note that calling setCurrentRollupState() in nested
* for loops (which is effectively what happens in rollups) will have an impact on performance when debugging is enabled.
*/
public class CRLP_Debug_UTIL {

    public static final Integer LEVEL_MIN = 1;
    public static final Integer LEVEL_MAX = 2;

    /*
     * @description Rather than package the Customizable_Rollup_Settings__c.Debug_Level__c field, which will make it harder
     * to remove at a later point, this requries that an admin (or sfdo staff) manually create the new custom settings field
     * on this object as an unmanaged field. The code below attempts to check for the field and if it exists will use it
     * to set the current debugging level. No field or a value of 0 or null means there CRLP Debugging is disabled.
     * Level 0 = OFF
     * Level 1 = MINIMAL
     * Level 2 = DETAILED
     */
    @TestVisible
    public static Integer debuggingLevel {
        get {
            if (debuggingLevel == null) {
                Customizable_Rollup_Settings__c crlpSettings = UTIL_CustomSettingsFacade.getCustomizableRollupSettings();
                try {
                    debuggingLevel = ((Double) crlpSettings.get('Debug_Level__c')).intValue();
                } catch (Exception ex) {
                    debuggingLevel = 0;
                }
            }
            return debuggingLevel;
        } private set;
    }

    /**
     * @description Meant to be used externally to determine when debugging is enabled
     */
    @TestVisible
    public static Boolean isDebuggingEnabled {
        get {
            return (debuggingLevel > 0);
        } private set;
    }

    private static List<String> currentRollupState = new List<String>();

    public static void clearCurrentRollupState() {
        if (isDebuggingEnabled) {
            currentRollupState.clear();
        }
    }

    public static void setCurrentRollupState(String state) {
        if (isDebuggingEnabled) {
            UTIL_Debug.debug('===== setCurrentRollupState(' + state + ')\n');
            currentRollupState.add(state);
        }
    }

    public static void amendLastCurrentRollupState(String state) {
        if (isDebuggingEnabled) {
            String lastStateVal = currentRollupState[currentRollupState.size() - 1];
            UTIL_Debug.debug('===== setCurrentRollupState(' + lastStateVal + ' ' + state + ')');
            currentRollupState[currentRollupState.size() - 1] = lastStateVal + ' ' + state;
        }
    }

    public static void setCurrentRollupState(String state, CRLP_Rollup rollup) {
        if (isDebuggingEnabled) {
            String rollupData = '';
            for (CRLP_Rollup.Rollupmdt rcmt : rollup.rollupsMdt) {
                rollupData += rcmt.summaryObject + '.' + rcmt.summaryField + '-' + rcmt.operation + ';';
            }
            currentRollupState.add(state + ' ==> Rollup(' + rollupData.removeEnd(';') + ')');
        }
    }

    public static String getCurrentRollupState() {
        String concatenatedRollupState = '';
        if (isDebuggingEnabled) {
            for (String rs : currentRollupState) {
                if (!rs.startsWith(' ')) {
                    concatenatedRollupState += '* ' + rs + '\n';
                } else {
                    concatenatedRollupState += '  ' + rs + '\n';
                }
            }
        }
        return concatenatedRollupState;
    }

    private static String getRollupCurrentValues(CRLP_Rollup rlp) {
        String debugText = null;
        if (debuggingLevel != 0) {
            debugText =
                '\n* # of MDT records=' + rlp.rollupsMdt.size() +
                '\n* detail=' + rlp.detailObject +
                '\n* theCount=' + rlp.theCount +
                '\n* theSum=' + rlp.theSum +
                '\n* minDateTime=' + rlp.minDateTime +
                '\n* maxDateTime=' + rlp.maxDateTime +
                '\n* minByYear=' + JSON.serialize(rlp.minByYear) +
                '\n* maxByYear=' + JSON.serialize(rlp.maxByYear) +
                '\n* sumByYear=' + JSON.serialize(rlp.sumByYear) +
                '\n* countByYear=' + JSON.serialize(rlp.countByYear) +
                (rlp.isDaysAgoOperation ? '\n* DaysAgoOperation=' + rlp.daysBack : '') +
                (rlp.isYearsAgoSingleResult ? '\n* YearsAgoSingleResult=' + rlp.yearsAgo : '');
            for (CRLP_Rollup.Rollupmdt r : rlp.rollupsMdt) {
                debugText += '\n   -- ' + r.summaryObject + '.' + r.summaryField + ' [' + r.resultFieldDisplayType + ']'
                    + (r.singleResultRollupType ? '[SingleResult]=' + r.getResultValue() : '');
            }
            debugText += '\n==================================';
        }
        return debugText;
    }

    public static String getRollupState(List<CRLP_Rollup> rollups) {
        String theState = '';
        if (isDebuggingEnabled) {
            Integer numRollupFields = 0;
            for (CRLP_Rollup r : rollups) {
                numRollupFields += r.rollupsMdt.size();
            }
            theState += '\n******************************************************' +
                '\nNumber of Rollup Fields: ' + numRollupFields +
                '\nNumber of Rollup Instances: ' + rollups.size() +
                '\n==================================';
            for (CRLP_Rollup r : rollups) {
                theState += getRollupCurrentValues(r) + '\n';
            }
        }
        return theState;
    }
}