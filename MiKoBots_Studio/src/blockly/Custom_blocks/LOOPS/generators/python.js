

python.pythonGenerator.forBlock['controls_repeat_ext1'] = function(block, generator) {
    // Repeat n times.
    let repeats;
    if (block.getField('TIMES')) {
        // Internal number.
        repeats = String(parseInt(block.getFieldValue('TIMES'), 10));
    }
    else {
        // External number.
        repeats = generator.valueToCode(block, 'TIMES', python.Order.NONE) || '0';
    }
    if (stringUtils.isNumber(repeats)) {
        repeats = parseInt(repeats, 10);
    }
    else {
        repeats = 'int(' + repeats + ')';
    }
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block) || generator.PASS;
    const loopVar = generator.nameDB_.getDistinctName('count', NameType.VARIABLE);

    const code = 'for ' + loopVar + ' in range(' + repeats + '):\n' + branch;
    return code;
}

python.pythonGenerator.forBlock['controls_whileUntil1'] = function(block, generator) {
    // Do while/until loop.
    const until = block.getFieldValue('MODE') === 'UNTIL';
    let argument0 = generator.valueToCode(block, 'BOOL', until ? python.Order.LOGICAL_NOT : python.Order.NONE) || 'False';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block) || generator.PASS;
    if (until) {
        argument0 = 'not ' + argument0;
    }
    
    const indentedBranch = `${generator.INDENT}time.sleep(0.01)\n${branch}`;
    const code = `while ${argument0}:\n${indentedBranch}`;
    return code;
}



python.pythonGenerator.forBlock['controls_for1'] = function(block, generator) {
    // For loop.
    const variable0 = generator.getVariableName(block.getFieldValue('VAR'));
    let argument0 = generator.valueToCode(block, 'FROM', python.Order.NONE) || '0';
    let argument1 = generator.valueToCode(block, 'TO', python.Order.NONE) || '0';
    let increment = generator.valueToCode(block, 'BY', python.Order.NONE) || '1';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block) || generator.PASS;
    let code = '';
    let range;
    // Helper functions.
    const defineUpRange = function () {
        return generator.provideFunction_('upRange', `
            def ${generator.FUNCTION_NAME_PLACEHOLDER_}(start, stop, step):
            while start <= stop:
                yield start
                start += abs(step)
            `);
    };
    const defineDownRange = function () {
        return generator.provideFunction_('downRange', `
            def ${generator.FUNCTION_NAME_PLACEHOLDER_}(start, stop, step):
            while start >= stop:
                yield start
                start -= abs(step)
            `);
    };
    // Arguments are legal generator code (numbers or strings returned by scrub()).
    const generateUpDownRange = function (start, end, inc) {
        return ('(' +
            start +
            ' <= ' +
            end +
            ') and ' +
            defineUpRange() +
            '(' +
            start +
            ', ' +
            end +
            ', ' +
            inc +
            ') or ' +
            defineDownRange() +
            '(' +
            start +
            ', ' +
            end +
            ', ' +
            inc +
            ')');
    };
    if (stringUtils.isNumber(argument0) &&
        stringUtils.isNumber(argument1) &&
        stringUtils.isNumber(increment)) {
        // All parameters are simple numbers.
        argument0 = Number(argument0);
        argument1 = Number(argument1);
        increment = Math.abs(Number(increment));
        if (argument0 % 1 === 0 && argument1 % 1 === 0 && increment % 1 === 0) {
            // All parameters are integers.
            if (argument0 <= argument1) {
                // Count up.
                argument1++;
                if (argument0 === 0 && increment === 1) {
                    // If starting index is 0, omit it.
                    range = argument1;
                }
                else {
                    range = argument0 + ', ' + argument1;
                }
                // If increment isn't 1, it must be explicit.
                if (increment !== 1) {
                    range += ', ' + increment;
                }
            }
            else {
                // Count down.
                argument1--;
                range = argument0 + ', ' + argument1 + ', -' + increment;
            }
            range = 'range(' + range + ')';
        }
        else {
            // At least one of the parameters is not an integer.
            if (argument0 < argument1) {
                range = defineUpRange();
            }
            else {
                range = defineDownRange();
            }
            range += '(' + argument0 + ', ' + argument1 + ', ' + increment + ')';
        }
    }
    else {
        // Cache non-trivial values to variables to prevent repeated look-ups.
        const scrub = function (arg, suffix) {
            if (stringUtils.isNumber(arg)) {
                // Simple number.
                arg = String(Number(arg));
            }
            else if (!arg.match(/^\w+$/)) {
                // Not a variable, it's complicated.
                const varName = generator.nameDB_.getDistinctName(variable0 + suffix, NameType.VARIABLE);
                code += `${varName} = ${arg}'\n'`;
                arg = varName;
            }
            return arg;
        };
        const startVar = scrub(argument0, '_start');
        const endVar = scrub(argument1, '_end');
        const incVar = scrub(increment, '_inc');
        if (typeof startVar === 'number' && typeof endVar === 'number') {
            if (startVar < endVar) {
                range = defineUpRange();
            }
            else {
                range = defineDownRange();
            }
            range += `(${startVar}, ${endVar}, ${incVar})`;
        }
        else {
            // We cannot determine direction statically.
            range = generateUpDownRange(startVar, endVar, incVar);
        }
    }
    code += `for ${variable0} in ${range}:\n${branch}`;

    return code;
}


python.pythonGenerator.forBlock['controls_forEach1'] = function(block, generator) {
    // For each loop.
    const variable0 = generator.getVariableName(block.getFieldValue('VAR'));
    const argument0 = generator.valueToCode(block, 'LIST', python.Order.RELATIONAL) || '[]';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block) || generator.PASS;
    const code = 'for ' + variable0 + ' in ' + argument0 + ':\n' + branch;
    return code;
}

python.pythonGenerator.forBlock['controls_flow_statements1'] = function(block, generator) {
    // Flow statements: continue, break.
    let xfix = '';
    if (generator.STATEMENT_PREFIX) {
        // Automatic prefix insertion is switched off for this block.  Add manually.
        xfix += generator.injectId(generator.STATEMENT_PREFIX, block);
    }
    if (generator.STATEMENT_SUFFIX) {
        // Inject any statement suffix here since the regular one at the end
        // will not get executed if the break/continue is triggered.
        xfix += generator.injectId(generator.STATEMENT_SUFFIX, block);
    }
    if (generator.STATEMENT_PREFIX) {
        const loop = block.getSurroundLoop();
        if (loop && !loop.suppressPrefixSuffix) {
            // Inject loop's statement prefix here since the regular one at the end
            // of the loop will not get executed if 'continue' is triggered.
            // In the case of 'break', a prefix is needed due to the loop's suffix.
            xfix += generator.injectId(generator.STATEMENT_PREFIX, loop);
        }
    }
    switch (block.getFieldValue('FLOW')) {
        case 'BREAK':
            return xfix + 'break\n';
        case 'CONTINUE':
            return xfix + 'continue\n';
    }
    throw Error('Unknown flow statement.');
}
//# sourceMappingURL=loops.js.map


const stringUtils = {
    isNumber: function(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }
};

const NameType = {
    VARIABLE: 'VARIABLE',
    PROCEDURE: 'PROCEDURE',
    // Add other name types if needed
};